import requests
import logging
import os
import socket
import pyaudio
import time
import threading
import warnings

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Fork:
    def __init__(self, api_key, base_url='http://3.93.16.238:5000'):
        self.api_key = api_key
        self.base_url = base_url
        self.state_machine = self.StateMachine()

    def fork(self, id, file_paths, isolated_voice_path, description=''):
        url = f"{self.base_url}/process"
        headers = {
            'key': self.api_key,
            'request-type': 'ADD_USER',
            'voice_description': description
        }
        files = [('files[]', open(file_path, 'rb'))
                 for file_path in file_paths]
        data = {'voice': id}

        logger.info("Sending request to %s with voice name %s and description %s",
                    url, id, description)

        try:
            response = requests.post(
                url, files=files, headers=headers, data=data)

            for _, file_handle in files:
                file_handle.close()

            logger.info("Received response with status code %d",
                        response.status_code)

            if response.status_code == 200:
                logger.info("Request successful: %s", response.json())
                return response.json()
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Request failed: %s", str(e))
            return None

    class StateMachine:
        def __init__(self):
            self.INIT = 'INIT'
            self.PRE_OP = 'PRE-OP'
            self.FAULT = 'FAULT'
            self.OPERATIONAL = 'OPERATIONAL'

            self.current_state = self.INIT
            self.errors = []
            self.active_time = 0
            self._running = False
            self._lock = threading.Lock()
            logger.info("State machine initialized in state: %s",
                        self.current_state)
            self._check_initialization_conditions()

        def _check_initialization_conditions(self):
            if not self._is_microphone_accessible():
                self.errors.append("Microphone not accessible")
            if not self._is_speaker_accessible():
                self.errors.append("Speaker not accessible")
            if not self._is_connected_to_wifi():
                self.errors.append("Not connected to Wi-Fi")

            if self.errors:
                self.transition_state(self.FAULT)
            else:
                self.transition_state(self.PRE_OP)

        def _is_microphone_accessible(self):
            logger.info("Looking for input audio source...")
            try:
                p = pyaudio.PyAudio()
                for i in range(p.get_device_count()):
                    dev = p.get_device_info_by_index(i)
                    if dev['maxInputChannels'] > 0:
                        p.terminate()
                        return True
                p.terminate()
                return False
            except Exception as e:
                logger.error("Microphone check failed: %s", str(e))
                return False

        def _is_speaker_accessible(self):
            logger.info("Looking for output audio source...")
            try:
                p = pyaudio.PyAudio()
                for i in range(p.get_device_count()):
                    dev = p.get_device_info_by_index(i)
                    if dev['maxOutputChannels'] > 0:
                        p.terminate()
                        return True
                p.terminate()
                return False
            except Exception as e:
                logger.error("Speaker check failed: %s", str(e))
                return False

        def _is_connected_to_wifi(self):
            logger.info("Checking for Wi-Fi connection...")
            try:
                socket.create_connection(("www.google.com", 80))
                return True
            except OSError:
                return False

        def transition_state(self, new_state):
            valid_transitions = {
                self.INIT: [self.PRE_OP, self.INIT, self.FAULT],
                self.PRE_OP: [self.OPERATIONAL, self.INIT, self.PRE_OP],
                self.FAULT: [self.INIT, self.FAULT],
                self.OPERATIONAL: [self.PRE_OP, self.OPERATIONAL]
            }
            if new_state in valid_transitions[self.current_state]:
                if self.current_state == self.FAULT:
                    self.errors.clear()
                logger.info("Changing state from %s to %s",
                            self.current_state, new_state)
                self.current_state = new_state
                logger.info("State changed to %s", self.current_state)
            else:
                warnings.warn(
                    f"Invalid state transition from {self.current_state} to {new_state}", RuntimeWarning)
                self.current_state = self.FAULT
                logger.error(
                    "State transitioned to FAULT due to invalid transition")

        def get_state(self):
            return self.current_state

        def get_errors(self):
            return self.errors

        def init(self):
            self._running = True
            self.active_time = 0
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

        def _run(self):
            while self._running:
                with self._lock:
                    self.active_time += 1
                    logger.info("Active time: %s seconds, Current state: %s",
                                self.active_time, self.current_state)
                time.sleep(1)

        def close(self):
            with self._lock:
                self._running = False
                if self._thread:
                    self._thread.join()
                self.transition_state(self.INIT)
                self.errors.clear()
                self.active_time = 0
                logger.info("State machine closed and reset to INIT state")


if __name__ == "__main__":
    fork_instance = Fork(api_key="PLACEHOLDER")
    fork_instance.state_machine.init()
    time.sleep(20)
    fork_instance.state_machine.transition_state(
        fork_instance.state_machine.PRE_OP)
    fork_instance.state_machine.transition_state(
        fork_instance.state_machine.INIT)
    time.sleep(10)
    fork_instance.state_machine.close()
    print("Current state:", fork_instance.state_machine.state())
    print("Errors:", fork_instance.state_machine.get_errors())
