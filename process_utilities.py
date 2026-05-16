"""Application process and listener management utilities."""

import re
import subprocess
import time

from .errors import ProcessStateError

SPEECH_JOIN_TIMEOUT_SECONDS = 5
TERMINATE_TIMEOUT_SECONDS = 1


def is_running(process):
    """Determine if a process is currently running."""
    image = process + ".exe"
    output = subprocess.check_output(
        ["tasklist", "/fi", "imagename eq " + image]
    )
    return bool(re.search(image, str(output)))


def wait_listeners(
    stop_listeners_event,
    process,
    mouse_listener,
    keyboard_listener,
    base_manager,
    speech_manager,
    speaking_process,
    indicator_thread=None,
    is_persistent=False,
):
    """Wait for listeners until the stop event is set or process ends."""
    while not stop_listeners_event.is_set():
        if is_running(process) or is_persistent:
            time.sleep(1)
        else:
            stop_listeners(
                mouse_listener,
                keyboard_listener,
                base_manager,
                speech_manager,
                speaking_process,
                indicator_thread=indicator_thread,
            )
            break


def stop_listeners(
    mouse_listener,
    keyboard_listener,
    base_manager,
    speech_manager,
    speaking_process,
    indicator_thread=None,
    speech_join_timeout=SPEECH_JOIN_TIMEOUT_SECONDS,
):
    """Stop all listeners and shutdown the managers."""
    if mouse_listener:
        mouse_listener.stop()
    if keyboard_listener:
        keyboard_listener.stop()
    if base_manager and speech_manager and speaking_process:
        if speech_manager.get_speech_text():
            time.sleep(0.01)

        try:
            speech_manager.set_can_speak(False)
            speaking_process.join(timeout=speech_join_timeout)
            if speaking_process.is_alive():
                speaking_process.terminate()
                speaking_process.join(timeout=TERMINATE_TIMEOUT_SECONDS)
                raise ProcessStateError(
                    "Speech process did not stop within "
                    f"{speech_join_timeout} seconds."
                )
        finally:
            base_manager.shutdown()
    if indicator_thread:
        indicator_thread.stop()
