"""Example using ctypes pulse structures.

  1) Two structures are built from scratch using their ctypes types.
  2) pa_stream_new() is called using pointers to these structures and returns
     an opaque pointer.
  3) pa_stream_get_sample_spec() returns a ctypes pointer that is used to
     build a PulseStructure instance. The type of a PulseStructure instance is
     a mapping type and printing its content shows that it matches the content
     of the pa_sample_spec structure used to create the stream.

Note:
-----
pa_stream_get_sample_spec() is a plain function (not a coroutine method of the
LibPulse instance) and the PulseStructure instantiation must be done
manually. This is not needed for the methods of the LibPulse instance whose
async functions return a structure or a list of structures.

"""

import sys
import asyncio
import ctypes as ct
from libpulse.libpulse import (LibPulse, PulseStructure, struct_ctypes,
                               pa_stream_new, pa_stream_unref,
                               pa_stream_get_sample_spec,
                               )

async def main():
    async with LibPulse('my libpulse') as lib_pulse:
        # Build the pa_sample_spec structure.
        c_sample_spec = struct_ctypes['pa_sample_spec'](3, 44100, 2)

        # Build the pa_channel_map structure.
        channel_labels = [0] * 32
        channel_labels[0] = 1
        channel_labels[1] = 2
        C_MAP = ct.c_int * 32
        c_map = C_MAP(*channel_labels)
        c_channel_map = struct_ctypes['pa_channel_map'](2, c_map)

        # Create the stream.
        c_pa_stream = pa_stream_new(lib_pulse.c_context, b'some name',
                                    ct.byref(c_sample_spec),
                                    ct.byref(c_channel_map))

        # From the ctypes documentation: "NULL pointers have a False
        # boolean value".
        if not bool(c_pa_stream):
            print('Error: cannot create a new stream', file=sys.stderr)
            sys.exit(1)

        try:
            # Get the pa_sample_spec structure as a PulseStructure instance.
            c_sample_spec = pa_stream_get_sample_spec(c_pa_stream)
            sample_spec = PulseStructure(c_sample_spec.contents,
                                         struct_ctypes['pa_sample_spec'])

            # Print the attributes of sample_spec.
            # This will print:
            #   {'format': 3, 'rate': 44100, 'channels': 2}
            print(sample_spec.__dict__)
        finally:
            pa_stream_unref(c_pa_stream)

asyncio.run(main())
