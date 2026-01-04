import ctypes
import llama_cpp

# C signature:
# void callback(int level, const char * message, void * user_data)
_LOG_CALLBACK_TYPE = ctypes.CFUNCTYPE(
    None,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_void_p,
)

# Keep a module-level reference so it is NOT garbage-collected
_silent_callback_ref = None


def disable_llama_logging():
    """
    Disable all native llama.cpp / ggml logging (Metal, CUDA, CPU).

    Must be called once, before creating any Llama instances.
    """
    global _silent_callback_ref

    def _silent_log(level, message, user_data):
        return

    _silent_callback_ref = _LOG_CALLBACK_TYPE(_silent_log)
    llama_cpp.llama_log_set(_silent_callback_ref, None)
