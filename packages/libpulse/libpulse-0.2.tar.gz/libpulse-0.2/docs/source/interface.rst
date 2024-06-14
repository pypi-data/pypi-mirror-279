Interface
=========

Overview
--------

The ``libpulse_ctypes`` module uses the ``pulse_types``, ``pulse_enums``,
``pulse_structs`` and ``pulse_functions`` modules of the libpulse package to
build:

  - The libpulse ctypes foreign functions corresponding to the ``pulse``
    functions.
  - The subclasses of the ctypes Structure corresponding to the ``pulse``
    structures.
  - The constants corresponding to the enums of the ``pulse`` library.

These four modules are generated from the headers of the ``pulse`` library and
may be re-generated using ``gcc`` and ``pyclibrary`` as explained in the
:ref:`Development` section, although this is not necessary. The ABI of the
``pulse`` library is pretty much stable and using recent versions of Pulseaudio
and Pipewire generates exactly the same modules.

The following sections describe the ``libpulse`` module of the libpulse package
that provides the whole ctypes interface to the library.

Variables
---------

The ``pulse`` enums constants are defined as variables in the ``libpulse``
module namespace. The ``PA_INVALID_INDEX`` variable is also defined there.

``CTX_STATES``
  Dictionary mapping the values of the ``pa_context_state`` enums with their
  string representation. For example CTX_STATES[0] is
  ``'PA_CONTEXT_UNCONNECTED'``.

``ERROR_CODES``
  Dictionary mapping the values of the ``pa_error_code`` enums with their
  string representation. For example ERROR_CODES[0] is ``'PA_OK'``.

``struct_ctypes``
  Dictionary of all the ``pulse`` structures defined as subclasses of the ctypes
  Structure.

Functions
---------

The ``pulse`` functions that are not async functions [#]_ have their
corresponding ctypes foreign functions defined in the ``libpulse`` module
namespace. They may be called directly once the LibPulse class has been
instantiated.

Async functions are implemented as methods of the LibPulse instance. They are
asyncio coroutines, see below.

Structures
----------

PulseStructure class
""""""""""""""""""""

A PulseStructure is instantiated with:

  - A ctypes pointer that is dereferenced using its ``contents`` attibute.
  - The subclass of ctypes Structure that corresponds to the type of this
    pointer which is found in the ``struct_ctypes`` dict.

A PulseStructure instance includes its nested structures and  the structures
that are referenced by a member of the  structure that is a pointer to another
structure (recursively). The attributes of the PulseStructure instance are the
names of the members of the ``pulse`` structure.

Using structures
""""""""""""""""

  non async functions
    `examples/pa_stream_new.py`_ shows how to create instances of two structures
    and pass their pointers to ``pa_stream_new()`` using ``struct_ctypes``.

    The example shows also how to build a PulseStructure from a pointer returned
    by ``pa_stream_get_sample_spec()``.

  async functions
    When a callback sets a pointer to a ``pulse`` structure as one of its
    arguments, the memory referenced by this pointer is very short-lived. A
    PulseStructure is then instantiated to make a deep copy of the structure.

    The PulseStructure instance is returned by the asyncio coroutine that
    handles this callback. See below how to call a ``pulse`` async function.

PropList class
""""""""""""""

When the member of a ``pulse`` structure is a pointer to a ``proplist``, the
corresponding PulseStructure attribute is set to an instance of PropList
class. The PropList class is a subclass of ``dict`` and the elements of the
proplist can be
accessed as the elements of a dictionary.

PulseEvent class
----------------

An instance of PulseEvent is returned by the async iterator returned by the
get_events() method of a LibPulse instance. See below
:ref:`pa_context_subscribe()`.

Its attributes are::

  facility:   str - name of the facility, for example 'sink'.
  index:      int - index of the facility.
  type:       str - type of event, 'new', 'change' or 'remove'.

LibPulse class
--------------

The LibPulse class is an asyncio context manager. To instantiate the LibPulse
instance run::

  async with LibPulse('some name') as lib_pulse:
    statements using the 'lib_pulse' LibPulse instance
    ...

A LibPulse instance manages the connection to the ``pulse`` library. There is
only one instance of this class per asyncio event loop, and therefore only one
instance per thread.

Attributes
""""""""""

``c_context``
  Required by non async functions prefixed with ``pa_context_`` as their first
  argument. Note that this first argument is excluded from the LibPulse async
  methods, see below.

``loop``
  The asyncio loop.

``state``
  The ``pulse`` context state. A tuple whose first element is one of the
  constants of the ``pa_context_state`` enum as a string, and the second and
  last one is one of the constants of the ``pa_error_code`` enum as a string. 

Methods
"""""""

The ``pulse`` async functions [1]_ are implemented as LibPulse methods that are
asyncio coroutines except for five :ref:`Not implemented` methods.

See `examples/pa_context_load_module.py`_.

These methods are sorted in four lists according to their signature and the
signature of their callbacks. These lists are the LibPulse class attributes:

  - context_methods
  - context_success_methods
  - context_list_methods
  - stream_success_methods

Methods arguments
"""""""""""""""""

The type of the first argument of the ``pulse`` async functions whose name
starts with ``pa_context`` is ``pa_context *``. This argument is **omitted**
upon invocation of the corresponding LibPulse method (the Libpulse instance
already knows it as one of its attributes named ``c_context``).

The type of the penultimate argument of the ``pulse`` async functions is the
type of the callback. This argument is **omitted** upon invocation of the
corresponding LibPulse method as the Libpulse instance already knows this type
from the signature of the function in the ``pulse_functions`` module and the
callback is implemented as an embedded function in the method definition.

The type of the last argument of the ``pulse`` async functions is ``void *`` and
the argument is meant to be used to match the  callback invocation with the
``pulse`` function that triggered it when the implementation is done in C
language. This last argument is not needed and **omitted** upon invocation of
the corresponding LibPulse method (the callback is implemented as an embedded
function in the method definition, more details at :ref:`Callbacks`).

For example pa_context_get_server_info() is invoked as:

.. code-block:: python

    server_info = await lib_pulse.pa_context_get_server_info()

Methods return value
""""""""""""""""""""

The ``context_methods`` return an empty list if the callback has no other
argument than ``pa_context *c`` and ``void *userdata``, they return a list if
the callback has set more than one of its arguments, otherwise they return the
unique argument set by the callback.

The ``context_success_methods`` and ``stream_success_methods`` return an
``int``, either PA_OPERATION_DONE or
PA_OPERATION_CANCELLED. PA_OPERATION_CANCELLED occurs as a result of the context
getting disconnected while the operation is pending.

The ``context_list_methods`` return a list after the ``pulse`` library has
invoked repeatedly the callback. The callback is invoked only once for methods
whose name ends with ``by_name`` or ``by_index`` and the result returned by
those coroutines in that case is this single element instead of the list.

.. _pa_context_subscribe():

pa_context_subscribe()
""""""""""""""""""""""

``pa_context_subscribe()`` is one of the LibPulse async method. This
method may be invoked at any time to change the subscription masks currently
set, even from within the ``async for`` loop that iterates over the reception of
libpulse events. After this method has been invoked for the first time, call the
``get_events()`` method to get an async iterator that returns the successive
libpulse events.

For example:

.. code-block:: python

    # Start the iteration on sink-input events.
    await lib_pulse.pa_context_subscribe(PA_SUBSCRIPTION_MASK_SINK_INPUT)
    iterator = lib_pulse.get_events()
    async for event in iterator:
        await handle_the_event(event)

``event`` is an instance of PulseEvent.

See also `examples/pa_context_subscribe.py`_.

.. _Not implemented:

Not implemented
"""""""""""""""

The following ``pulse`` async functions are not implemented as a method of a
LibPulse instance:

    pa_signal_new() and pa_signal_set_destroy():
        Signals are handled by asyncio and the hook signal support built into
        pulse abstract main loop is not needed.

In the following functions the callback has to be handled by the libpulse module
user:

  - pa_context_rttime_new()
  - pa_stream_write()
  - pa_stream_write_ext_free()

An example on how to implement those coroutines can be found in the LibPulse
class implementation of context state monitoring:

    - ``__init__()`` sets the function pointer (and keeps a refence to it to
      prevent Python garbage collection) to a LibPulse staticmethod named
      ``context_state_callback()`` that will be called as the ``pulse``
      callback. The staticmethod gets the LibPulse instance through a call to
      the get_instance() method.

    - Upon entering the LibPulse context manager, the ``_pa_context_connect()``
      method sets this fonction pointer as the callback in the call to
      ``pa_context_set_state_callback()``.

.. _examples/pa_stream_new.py:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/examples/pa_stream_new.py?ref_type=heads#L1
.. _examples/pa_context_load_module.py:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/examples/pa_context_load_module.py?ref_type=heads#L1
.. _examples/pa_context_subscribe.py:
   https://gitlab.com/xdegaye/libpulse/-/blob/master/examples/pa_context_subscribe.py?ref_type=heads#L1

.. rubric:: Footnotes

.. [#] ``pulse`` async functions are those functions that have a callback as
       one of their arguments and that do not set the callback.
