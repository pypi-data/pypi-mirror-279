import time
from memoizelabs.client import Fork


def test_fork():
    utensil = Fork(api_key="PLACEHOLDER")
    forkupine = utensil.state_machine()
    forkupine.init()
    time.sleep(20)
    forkupine.transition_state(
        forkupine.PRE_OP)
    forkupine.transition_state(
        forkupine.INIT)
    time.sleep(10)
    forkupine.close()
    print("Current state:", forkupine.get_state())
    print("Errors:", forkupine.get_errors())


if __name__ == "__main__":
    test_fork()
