Asyncio interface to the Pulseaudio and Pipewire pulse library.

`libpulse`_ is a Python project based on `asyncio`_, that uses `ctypes`_ to
interface with the ``pulse`` library of the PulseAudio and PipeWire sound
servers. The interface is meant to be complete. That is, all the constants,
structures, plain functions and async functions are made available by importing
the libpulse module of the libpulse package.

Calling an async function is simple:

.. code-block:: python

    import asyncio
    from libpulse.libpulse import LibPulse

    async def main():
        async with LibPulse('my libpulse') as lib_pulse:
            server_info = await lib_pulse.pa_context_get_server_info()
            print(server_info)

    asyncio.run(main())

Another example processing sink-input events:

.. code-block:: python

    import asyncio
    from libpulse.libpulse import LibPulse, PA_SUBSCRIPTION_MASK_SINK_INPUT

    async def main():
        async with LibPulse('my libpulse') as lib_pulse:
            await lib_pulse.pa_context_subscribe(
                                            PA_SUBSCRIPTION_MASK_SINK_INPUT)
            iterator = lib_pulse.get_events()
            async for event in iterator:
                    some_function_to_process_the_event(event)

    asyncio.run(main())

See the libpulse `documentation`_.

Requirements
============

Python version 3.8 or more recent.

Installation
============

Install ``libpulse`` with pip::

  $ python -m pip install libpulse

.. _libpulse: https://gitlab.com/xdegaye/libpulse
.. _asyncio: https://docs.python.org/3/library/asyncio.html
.. _ctypes: https://docs.python.org/3/library/ctypes.html
.. _documentation: https://libpulse.readthedocs.io/en/stable/
