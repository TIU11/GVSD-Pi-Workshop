# suppress_alsa_warnings.py

import ctypes

def suppress():
    """Suppress ALSA and JACK warnings printed to stderr."""
    def py_error_handler(filename, line, function, err, fmt):
        pass

    try:
        c_error_handler = ctypes.CFUNCTYPE(
            None, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p
        )(py_error_handler)
        asound = ctypes.cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
    except Exception:
        pass
