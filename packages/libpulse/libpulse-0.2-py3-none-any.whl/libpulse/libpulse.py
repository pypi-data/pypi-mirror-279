"""ctypes interface to the pulse library based on asyncio."""

import sys
import asyncio
import logging
import re
import pprint
import ctypes as ct
from functools import partialmethod

from .libpulse_ctypes import PulseCTypes, PA_INVALID_INDEX
from .mainloop import MainLoop, pulse_ctypes, callback_func_ptr
from .pulse_functions import pulse_functions
from .pulse_enums import pulse_enums

struct_ctypes = pulse_ctypes.struct_ctypes
logger = logging.getLogger('libpuls')

def _add_pulse_to_namespace():
    def add_obj(name, obj):
        assert getattr(module, name, None) is None, f'{name} is duplicated'
        setattr(module, name, obj)

    # Add the pulse constants and functions to the module namespace.
    module = sys.modules[__name__]

    for name in pulse_functions['signatures']:
        func = pulse_ctypes.get_prototype(name)
        add_obj(name, func)

    for enum, constants in pulse_enums.items():
        for name, value in constants.items():
            add_obj(name, value)
_add_pulse_to_namespace()
del _add_pulse_to_namespace

# Map values to their name.
ERROR_CODES = dict((eval(var), var) for var in globals() if
                   var.startswith('PA_ERR_') or var == 'PA_OK')
CTX_STATES = dict((eval(state), state) for state in
                  ('PA_CONTEXT_UNCONNECTED', 'PA_CONTEXT_CONNECTING',
                   'PA_CONTEXT_AUTHORIZING', 'PA_CONTEXT_SETTING_NAME',
                   'PA_CONTEXT_READY', 'PA_CONTEXT_FAILED',
                   'PA_CONTEXT_TERMINATED'))

def event_codes_to_names():
    def build_events_dict(mask):
        for fac in globals():
            if fac.startswith(prefix):
                val = eval(fac)
                if (val & mask) and val != mask:
                    yield val, fac[prefix_len:].lower()

    prefix = 'PA_SUBSCRIPTION_EVENT_'
    prefix_len = len(prefix)
    facilities = {0 : 'sink'}
    facilities.update(build_events_dict(PA_SUBSCRIPTION_EVENT_FACILITY_MASK))
    event_types = {0: 'new'}
    event_types.update(build_events_dict(PA_SUBSCRIPTION_EVENT_TYPE_MASK))
    return facilities, event_types

# Dictionaries mapping libpulse events values to their names.
EVENT_FACILITIES, EVENT_TYPES = event_codes_to_names()

def run_in_task(coro):
    """Decorator to wrap a coroutine in a task of AsyncioTasks instance."""

    async def wrapper(*args, **kwargs):
        lib_pulse = LibPulse.get_instance()
        if lib_pulse is None:
            raise LibPulseClosedError

        try:
            return await lib_pulse.libpulse_tasks.create_task(
                                                    coro(*args, **kwargs))
        except asyncio.CancelledError:
            logger.error(f'{coro.__qualname__}() has been cancelled')
            raise
    return wrapper

class LibPulseError(Exception): pass
class LibPulseClosedError(LibPulseError): pass
class LibPulseStateError(LibPulseError): pass
class LibPulseOperationError(LibPulseError): pass
class LibPulseClosedIteratorError(LibPulseError): pass
class LibPulseInstanceExistsError(LibPulseError): pass
class LibPulseArgumentError(LibPulseError): pass

class EventIterator:
    """Pulse events asynchronous iterator."""

    QUEUE_CLOSED = object()

    def __init__(self):
        self.event_queue = asyncio.Queue()
        self.closed = False

    # Public methods.
    def close(self):
        self.closed = True

    # Private methods.
    def abort(self):
        while True:
            try:
                self.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        self.put_nowait(self.QUEUE_CLOSED)

    def put_nowait(self, obj):
        if not self.closed:
            self.event_queue.put_nowait(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.closed:
            logger.info('Events Asynchronous Iterator is closed')
            raise StopAsyncIteration

        try:
            event = await self.event_queue.get()
        except asyncio.CancelledError:
            self.close()
            raise StopAsyncIteration

        if event is not self.QUEUE_CLOSED:
            return event
        self.close()
        raise LibPulseClosedIteratorError('Got QUEUE_CLOSED')

class AsyncioTasks:
    def __init__(self):
        self._tasks = set()

    def create_task(self, coro):
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(lambda t: self._tasks.remove(t))
        return task

    def __iter__(self):
        for t in self._tasks:
            yield t

class PulseEvent:
    """A libpulse event.

    Use the event_facilities() and event_types() static methods to get all the
    values currently defined by the libpulse library for 'facility' and
    'type'. They correspond to some of the variables defined in the
    pulse_enums module under the pa_subscription_event_type Enum.

    attributes:
        facility:   str - name of the facility, for example 'sink'.
        index:      int - index of the facility.
        type:       str - type of event, normaly 'new', 'change' or 'remove'.
    """

    def __init__(self, event_type, index):
        fac = event_type & PA_SUBSCRIPTION_EVENT_FACILITY_MASK
        assert fac in EVENT_FACILITIES
        self.facility = EVENT_FACILITIES[fac]

        type = event_type & PA_SUBSCRIPTION_EVENT_TYPE_MASK
        assert type in EVENT_TYPES
        self.type = EVENT_TYPES[type]

        self.index = index

    @staticmethod
    def event_facilities():
        return list(EVENT_FACILITIES.values())

    @staticmethod
    def event_types():
        return list(EVENT_TYPES.values())

class PropList(dict):
    """Dictionary of the elements of a proplist whose value is a string."""

    def __init__(self, c_pa_proplist):
        super().__init__()

        null_ptr = ct.POINTER(ct.c_void_p)()
        null_ptr_ptr = ct.pointer(null_ptr)
        while True:
            key = pa_proplist_iterate(c_pa_proplist, null_ptr_ptr)
            if isinstance(key, bytes):
                val = pa_proplist_gets(c_pa_proplist, key)
                if bool(val):
                    self[key.decode()] = val.decode()
            elif not bool(key):
                break

class PulseStructure:
    """The representation of a ctypes Structure.

    When returned by a callback as a pointer to a structure, one must make a
    deep copy of the elements of the structure as they are only temporarily
    available.
    """

    ignored_pointer_names = set()

    array_sizes = {
        'pa_card_port_info':        'n_ports',
        'pa_source_port_info':      'n_ports',
        'pa_sink_port_info':        'n_ports',
        'pa_card_profile_info':     'n_profiles',
        'pa_card_profile_info2':    'n_profiles',
        'pa_format_info':           'n_formats',
        }

    def __init__(self, c_struct, c_structure_type):
        for name, c_type in c_structure_type._fields_:
            fq_name = f'{c_structure_type.__name__}.{name}: {c_type.__name__}'
            if fq_name in self.ignored_pointer_names:
                continue

            try:
                c_struct_val = getattr(c_struct, name)
            except AttributeError:
                assert False, (f'{fq_name} not found while instantiating'
                               f' a PulseStructure')

            if c_type in PulseCTypes.numeric_types.values():
                setattr(self, name, c_struct_val)

            # A NULL pointer.
            elif not bool(c_struct_val):
                setattr(self, name, None)

            elif c_type is ct.c_char_p:
                setattr(self, name, c_struct_val.decode())

            # A proplist pointer.
            elif (isinstance(c_struct_val, ct._Pointer) and
                        c_struct_val._type_.__name__ == 'pa_proplist'):
                setattr(self, name, PropList(c_struct_val))

            # An array.
            elif isinstance(c_struct_val, ct.Array):
                # All libpulse arrays have a numeric type.
                setattr(self, name, c_struct_val[:])

            # An array of pointers.
            elif (isinstance(c_struct_val, ct._Pointer) and
                    isinstance(c_struct_val.contents, ct._Pointer)):
                ptr = c_struct_val.contents
                ctype = ptr._type_
                if ctype.__name__ in struct_ctypes:
                    val = []
                    size_attr = self.array_sizes[ctype.__name__]
                    array_size = getattr(self, size_attr)
                    i = 0
                    while True:
                        if not bool(ptr[i]):
                            break
                        if i == array_size:
                            break
                        val.append(PulseStructure(ptr[i], ctype))
                        i += 1
                    setattr(self, name, val)
                else:
                    self.ignore_member(fq_name)

            # A pointer.
            elif isinstance(c_struct_val, ct._Pointer):
                if c_struct_val._type_.__name__ in struct_ctypes:
                    setattr(self, name,
                            PulseStructure(c_struct_val.contents,
                                           c_struct_val._type_))
                else:
                    self.ignore_member(fq_name)

            # A structure.
            else:
                if c_type.__name__ in struct_ctypes:
                    setattr(self, name,
                            PulseStructure(c_struct_val, c_type))
                else:
                    self.ignore_member(fq_name)

    def ignore_member(self, name):
        self.ignored_pointer_names.add(name)
        logger.debug(f"Ignoring '{name}' structure member")

    def __repr__(self):
        return pprint.pformat(self.__dict__, sort_dicts=False)

class LibPulse:
    """Interface to libpulse library as an asynchronous context manager."""

    ASYNCIO_LOOPS = dict()              # {asyncio loop: LibPulse instance}

    # Function signature: (pa_operation *,
    #                      [pa_context *, [args...], cb_t, void *])
    # Callback signature: (void, [pa_context *, [objs...], void *])
    context_methods = (
        'pa_context_drain',
        'pa_context_get_server_info',
        'pa_context_load_module',
        'pa_context_play_sample_with_proplist',
        'pa_context_send_message_to_object',
        'pa_context_stat',
    )

    # Function signature: (pa_operation *,
    #                      [pa_context *, [args...], cb_t, void *])
    # Callback signature: (void, [pa_context *, int, void *])
    context_success_methods = (
        'pa_context_exit_daemon',
        'pa_context_kill_client',
        'pa_context_kill_sink_input',
        'pa_context_kill_source_output',
        'pa_context_move_sink_input_by_index',
        'pa_context_move_sink_input_by_name',
        'pa_context_move_source_output_by_index',
        'pa_context_move_source_output_by_name',
        'pa_context_play_sample',
        'pa_context_proplist_remove',
        'pa_context_proplist_update',
        'pa_context_remove_sample',
        'pa_context_set_card_profile_by_index',
        'pa_context_set_card_profile_by_name',
        'pa_context_set_default_sink',
        'pa_context_set_default_source',
        'pa_context_set_name',
        'pa_context_set_port_latency_offset',
        'pa_context_set_sink_input_mute',
        'pa_context_set_sink_input_volume',
        'pa_context_set_sink_mute_by_index',
        'pa_context_set_sink_mute_by_name',
        'pa_context_set_sink_port_by_index',
        'pa_context_set_sink_port_by_name',
        'pa_context_set_sink_volume_by_index',
        'pa_context_set_sink_volume_by_name',
        'pa_context_set_source_mute_by_index',
        'pa_context_set_source_mute_by_name',
        'pa_context_set_source_output_mute',
        'pa_context_set_source_output_volume',
        'pa_context_set_source_port_by_index',
        'pa_context_set_source_port_by_name',
        'pa_context_set_source_volume_by_index',
        'pa_context_set_source_volume_by_name',
        'pa_context_subscribe',
        'pa_context_suspend_sink_by_index',
        'pa_context_suspend_sink_by_name',
        'pa_context_suspend_source_by_index',
        'pa_context_suspend_source_by_name',
        'pa_context_unload_module',
    )

    # Function signature: (pa_operation *, [pa_context *, cb_t, void *])
    # Callback signature: (void, [pa_context *, struct *, int, void *])
    context_list_methods = (
        'pa_context_get_card_info_by_index',
        'pa_context_get_card_info_by_name',
        'pa_context_get_card_info_list',
        'pa_context_get_client_info',
        'pa_context_get_client_info_list',
        'pa_context_get_module_info',
        'pa_context_get_module_info_list',
        'pa_context_get_sample_info_by_index',
        'pa_context_get_sample_info_by_name',
        'pa_context_get_sample_info_list',
        'pa_context_get_sink_info_by_index',
        'pa_context_get_sink_info_by_name',
        'pa_context_get_sink_info_list',
        'pa_context_get_sink_input_info',
        'pa_context_get_sink_input_info_list',
        'pa_context_get_source_info_by_index',
        'pa_context_get_source_info_by_name',
        'pa_context_get_source_info_list',
        'pa_context_get_source_output_info',
        'pa_context_get_source_output_info_list',
    )

    # Function signature: (pa_operation *,
    #                      [pa_stream *, [args...], cb_t, void *])
    # Callback signature: (void, [pa_stream *, int, void *])
    stream_success_methods = (
        'pa_stream_cork',
        'pa_stream_drain',
        'pa_stream_flush',
        'pa_stream_prebuf',
        'pa_stream_proplist_remove',
        'pa_stream_proplist_update',
        'pa_stream_set_buffer_attr',
        'pa_stream_set_name',
        'pa_stream_trigger',
        'pa_stream_update_sample_rate',
        'pa_stream_update_timing_info',
    )

    def __init__(self, name):
        """'name' is the name of the application."""

        assert isinstance(name, str)
        self.loop = asyncio.get_running_loop()
        if self.loop in self.ASYNCIO_LOOPS:
            raise LibPulseInstanceExistsError

        self.c_context = pa_context_new(MainLoop.C_MAINLOOP_API,
                                        name.encode())
        # From the ctypes documentation: "NULL pointers have a False
        # boolean value".
        if not bool(self.c_context):
            raise RuntimeError('Cannot get context from libpulse library')

        self.closed = False
        self.state = ('PA_CONTEXT_UNCONNECTED', 'PA_OK')
        self.main_task = asyncio.current_task(self.loop)
        self.libpulse_tasks = AsyncioTasks()
        self.state_notification = self.loop.create_future()
        self.event_iterator = None
        self.ASYNCIO_LOOPS[self.loop] = self
        LibPulse.add_async_methods()

        # Keep a reference to prevent garbage collection.
        self.c_context_state_callback = callback_func_ptr(
            'pa_context_notify_cb_t', LibPulse.context_state_callback)
        self.c_context_subscribe_callback = callback_func_ptr(
            'pa_context_subscribe_cb_t', LibPulse.context_subscribe_callback)

    # Initialisation.
    @staticmethod
    def add_async_methods():
        # Register the partial methods.
        method_types = {
            'context_methods':          LibPulse._pa_context_get,
            'context_success_methods':  LibPulse._pa_context_op_success,
            'context_list_methods':     LibPulse._pa_context_get_list,
            'stream_success_methods':   LibPulse._pa_stream_op_success,
            }

        this_module = sys.modules[__name__]
        for method_type, libpulse_method in method_types.items():
            func_names = getattr(LibPulse, method_type)
            for func_name in func_names:
                setattr(LibPulse, func_name,
                                    partialmethod(libpulse_method, func_name))
                if hasattr(this_module, func_name):
                    delattr(this_module, func_name)

    @staticmethod
    def get_instance():
        loop = asyncio.get_running_loop()
        try:
            return LibPulse.ASYNCIO_LOOPS[loop]
        except KeyError:
            return None

    @staticmethod
    def context_state_callback(c_context, c_userdata):
        """Call back that monitors the connection state."""

        lib_pulse = LibPulse.get_instance()
        if lib_pulse is None:
            return

        st = pa_context_get_state(c_context)
        st = CTX_STATES[st]
        if st in ('PA_CONTEXT_READY', 'PA_CONTEXT_FAILED',
                     'PA_CONTEXT_TERMINATED'):
            error = pa_context_errno(c_context)
            error = ERROR_CODES[error]

            state = (st, error)
            logger.info(f'LibPulse connection: {state}')

            state_notification = lib_pulse.state_notification
            if not state_notification.done():
                state_notification.set_result(state)
            elif not lib_pulse.closed and st != 'PA_CONTEXT_READY':
                # A task is used here instead of calling directly abort() so
                # that pa_context_connect() has the time to handle a
                # previous PA_CONTEXT_READY state.
                asyncio.create_task(lib_pulse.abort(state))
        else:
            logger.debug(f'LibPulse connection: {st}')

    @run_in_task
    async def _pa_context_connect(self):
        """Connect the context to the default server."""

        pa_context_set_state_callback(self.c_context,
                                      self.c_context_state_callback, None)
        rc = pa_context_connect(self.c_context, None, PA_CONTEXT_NOAUTOSPAWN,
                                None)
        logger.debug(f'pa_context_connect return code: {rc}')
        await self.state_notification
        self.state = self.state_notification.result()

        if self.state[0] != 'PA_CONTEXT_READY':
            raise LibPulseStateError(self.state)

    @staticmethod
    def context_subscribe_callback(c_context, event_type, index, c_userdata):
        """Call back to handle pulseaudio events."""

        lib_pulse = LibPulse.get_instance()
        if lib_pulse is None:
            return

        if lib_pulse.event_iterator is not None:
            lib_pulse.event_iterator.put_nowait(PulseEvent(event_type,
                                                            index))


    # Libpulse async methods workers.
    @staticmethod
    def get_callback_data(func_name):
        # Get name and signature of the callback argument of 'func_name'.
        func_sig = pulse_functions['signatures'][func_name]
        args = func_sig[1]
        for arg in args:
            if arg in pulse_functions['callbacks']:
                callback_name = arg
                callback_sig = pulse_functions['callbacks'][arg]
                assert len(args) >= 3 and arg == args[-2]
                return callback_name, callback_sig

    def call_ctypes_func(self, func_name, operation_type, cb_func_ptr,
                         *func_args):
        # Call the 'func_name' ctypes function.
        args = []
        for arg in func_args:
            arg = arg.encode() if isinstance(arg, str) else arg
            args.append(arg)
        func_proto = pulse_ctypes.get_prototype(func_name)
        try:
            c_operation = func_proto(operation_type, *args, cb_func_ptr, None)
        except ct.ArgumentError as e:
            first_arg = ('c_context' if operation_type == self.c_context else
                         'pa_stream')
            raise LibPulseArgumentError(
                f"\nException reported by ctypes:\n"
                f"  {e!r}"
                f"\nFunction arguments:\n"
                f"  {func_name}{(first_arg, *args, cb_func_ptr, None)}\n"
                )
        return c_operation

    @staticmethod
    async def handle_operation(c_operation, future, errmsg):
        # From the ctypes documentation: "NULL pointers have a False
        # boolean value".
        if not bool(c_operation):
            future.cancel()
            raise LibPulseOperationError(errmsg)

        try:
            await future
        except asyncio.CancelledError:
            pa_operation_cancel(c_operation)
            raise
        finally:
            pa_operation_unref(c_operation)

    async def _pa_get(self, func_name, operation_type, *func_args):
        """Call an asynchronous pulse function that does not return a list.

        'func_args' is the sequence of the arguments of the function preceding
        the callback in the function signature. The last argument
        (i.e. 'userdata') is set to None by call_ctypes_func().
        """

        def callback_func(c_operation_type, *c_results):
            results = []
            for arg, c_result in zip(callback_sig[1][1:-1], c_results[:-1]):
                arg_list = arg.split()
                if arg_list[-1] == '*':
                    assert arg_list[0] in struct_ctypes
                    struct_name = arg_list[0]
                    if not bool(c_result):
                        results.append(None)
                    else:
                        results.append(PulseStructure(c_result.contents,
                                                struct_ctypes[struct_name]))
                else:
                    results.append(c_result)

            if not notification.done():
                notification.set_result(results)

        callback_data = self.get_callback_data(func_name)
        assert callback_data, f'{func_name} signature without a callback'
        callback_name, callback_sig = callback_data

        notification  = self.loop.create_future()
        errmsg = f'Error at {func_name}()'

        # Await on the future.
        cb_func_ptr = callback_func_ptr(callback_name, callback_func)
        c_operation = self.call_ctypes_func(func_name, operation_type,
                                                    cb_func_ptr, *func_args)
        await LibPulse.handle_operation(c_operation, notification, errmsg)

        results = notification.result()
        for result in results:
            if result is None:
                raise LibPulseOperationError(errmsg)
        if len(results) == 1:
            return results[0]
        return results

    @run_in_task
    async def _pa_context_get_list(self, func_name, *func_args):
        """Call an asynchronous pulse function that returns a list.

        'func_args' is the sequence of the arguments of the function preceding
        the callback in the function signature. The last argument
        (i.e. 'userdata') is set to None by call_ctypes_func().
        """

        def info_callback(c_context, c_info, eol, c_userdata):
            # From the ctypes documentation: "NULL pointers have a False
            # boolean value".
            if not bool(c_info):
                if not notification.done():
                    notification.set_result(eol)
            else:
                arg = callback_sig[1][1]
                arg_list = arg.split()
                assert arg_list[-1] == '*'
                assert arg_list[0] in struct_ctypes
                struct_name = arg_list[0]
                infos.append(PulseStructure(c_info.contents,
                                            struct_ctypes[struct_name]))

        callback_data = self.get_callback_data(func_name)
        assert callback_data, f'{func_name} signature without a callback'
        callback_name, callback_sig = callback_data

        infos = []
        notification  = self.loop.create_future()
        errmsg = f'Error at {func_name}()'

        # Await on the future.
        cb_func_ptr = callback_func_ptr(callback_name, info_callback)
        c_operation = self.call_ctypes_func(func_name, self.c_context,
                                                    cb_func_ptr, *func_args)
        await LibPulse.handle_operation(c_operation, notification, errmsg)

        eol = notification.result()
        if eol < 0:
            raise LibPulseOperationError(errmsg)
        if func_name.endswith(('_by_name', '_by_index')):
            assert len(infos) == 1
            return infos[0]
        return infos

    @run_in_task
    async def _pa_context_get(self, func_name, *func_args):
        return await self._pa_get(func_name, self.c_context, *func_args)

    @run_in_task
    async def _pa_context_op_success(self, func_name, *func_args):
        success = await self._pa_get(func_name, self.c_context, *func_args)
        if success == PA_OPERATION_CANCELLED:
            logger.debug(f'Got PA_OPERATION_CANCELLED for {func_name}')
        return success

    @run_in_task
    async def _pa_stream_op_success(self, func_name, stream, *func_args):
        success = await self._pa_get(func_name, stream, *func_args)
        if success == PA_OPERATION_CANCELLED:
            logger.debug(f'Got PA_OPERATION_CANCELLED for {func_name}')
        return success


    # Context manager.
    async def abort(self, state):
        # Cancelling the main task does close the LibPulse context manager.
        logger.error(f'The LibPulse instance has been aborted: {state}')
        self.main_task.cancel()

    def close(self):
        if self.closed:
            return
        self.closed = True

        try:
            for task in self.libpulse_tasks:
                task.cancel()
            if self.event_iterator is not None:
                self.event_iterator.abort()

            pa_context_set_state_callback(self.c_context, None, None)
            pa_context_set_subscribe_callback(self.c_context, None, None)

            if self.state[0] == 'PA_CONTEXT_READY':
                pa_context_disconnect(self.c_context)
                logger.info('Disconnected from libpulse context')
        finally:
            pa_context_unref(self.c_context)

            for loop, lib_pulse in list(self.ASYNCIO_LOOPS.items()):
                if lib_pulse is self:
                    del self.ASYNCIO_LOOPS[loop]
                    break
            else:
                logger.error('Cannot remove LibPulse instance upon closing')

            MainLoop.close()
            logger.debug('LibPulse instance closed')

    async def __aenter__(self):
        try:
            # Set up the two callbacks that live until this instance is
            # closed.
            self.main_task = asyncio.current_task(self.loop)
            await self._pa_context_connect()
            pa_context_set_subscribe_callback(self.c_context,
                                    self.c_context_subscribe_callback, None)
            return self
        except asyncio.CancelledError:
            self.close()
            if self.state[0] != 'PA_CONTEXT_READY':
                raise LibPulseStateError(self.state)
        except Exception:
            self.close()
            raise

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.close()
        if exc_type is asyncio.CancelledError:
            if self.state[0] != 'PA_CONTEXT_READY':
                raise LibPulseStateError(self.state)


    # Public methods.
    def get_events(self):
        """Return an Asynchronous Iterator of libpulse events.

        The iterator is used to run an async for loop over the PulseEvent
        instances. The async for loop can be terminated by invoking the
        close() method of the iterator from within the loop or from another
        task.
        """
        if self.closed:
            raise LibPulseOperationError('The LibPulse instance is closed')

        if self.event_iterator is not None and not self.event_iterator.closed:
            raise LibPulseError('Not allowed: the current Asynchronous'
                                ' Iterator must be closed first')
        self.event_iterator = EventIterator()
        return self.event_iterator

    async def log_server_info(self):
        if self.state[0] != 'PA_CONTEXT_READY':
            raise LibPulseStateError(self.state)

        server_info = await self.pa_context_get_server_info()
        server_name = server_info.server_name
        if re.match(r'.*\d+\.\d', server_name):
            # Pipewire includes the server version in the server name.
            logger.info(f'Server: {server_name}')
        else:
            logger.info(f'Server: {server_name} {server_info.server_version}')

        version = pa_context_get_protocol_version(self.c_context)
        server_ver = pa_context_get_server_protocol_version(self.c_context)
        logger.debug(f'libpulse library/server versions: '
                     f'{version}/{server_ver}')

        # 'server' is the name of the socket libpulse is connected to.
        server = pa_context_get_server(self.c_context)
        logger.debug(f'{server_name} connected to {server.decode()}')
