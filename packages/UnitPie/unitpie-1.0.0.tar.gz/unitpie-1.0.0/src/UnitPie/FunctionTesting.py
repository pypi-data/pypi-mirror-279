import sys
from typing import Optional
from .SubClassManagement import TestCase
import colorama

_do_nothing: callable = lambda: None
MainTests = TestCase("MainTests")

class _Test:
    def __init__(self, func: callable, setup: callable = _do_nothing, ParentTestCase: TestCase = MainTests):
        self.func: callable = func
        self.setup: callable = setup
        self.tc: TestCase = ParentTestCase

    def __eq__(self, other):
        return self.func == other.func and self.tc == other.tc

    def __hash__(self):
        return hash((self.func, self.tc))

    def run_test(self) -> bool:
        try:
            self.setup()
        except Exception as e:
            print("Error in setup function: ", end = '', file = sys.stderr)
            raise e

        try:
            self.func()
        except BaseException as _:
            return False
        return True


tests: set[_Test] = set()
ignored: set[callable] = set()

def test(setup: callable = _do_nothing, testcase: TestCase = MainTests):
    """To be used as a decorator to manually assign a function as a test to be run!"""
    def decorator(func: callable):
        """To be used as a decorator to manually assign a function as a test to be run!"""
        TEST = _Test(func, setup, testcase)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        tests.add(TEST)
        return wrapper
    return decorator

def ignore(func: callable):
    """To be used as a decorator to manually assign a function as a test to be run!"""
    ignored.add(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    return wrapper

def main(Globals: Optional[dict] = None) -> None:
    if not Globals:
        Globals = globals()
    """Runs all tests unless they are ignored"""
    outputs: dict[bool, str] = {
        True: f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}✔{colorama.Style.RESET_ALL} [PASSED]",
        False: f"{colorama.Style.BRIGHT}{colorama.Fore.RED}✖{colorama.Style.RESET_ALL} [FAILED]"
    }
    SETUP: callable = _do_nothing
    if Globals.get("setup"):
        SETUP = Globals.get("setup")

    alltests: set = tests
    for name, v in Globals.items():
        if not (name.startswith("__") or name.endswith("__")):
            if name.startswith("test") and (v not in ignored) and callable(v) and v != test:
                TEST = _Test(v, SETUP)
                alltests.add(TEST)

    TOTAL = len(alltests)
    PASSED: int = 0

    for i, v in enumerate(alltests):
        PERCENTAGE = (i + 1) * 100 // TOTAL
        if v.func not in ignored:
            print(f"{v.tc.name} :: {v.func.__name__} ------- ", end='')
            result: bool = v.run_test()
            if result:
                PASSED += 1
            print(outputs.get(result, f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}? [UNKNOWN]{colorama.Style.RESET_ALL}"), end = ' ')
            print(f"[{PERCENTAGE}%]")

    print('\n', end = '')
    FAILED: int = TOTAL - PASSED
    if FAILED == TOTAL:
        print(f"All {TOTAL} tests failed! [100%]")
    elif PASSED == TOTAL:
        print(f"All {TOTAL} tests passed! [100%]")
    else:
        print(f"{FAILED} ({FAILED * 100 // TOTAL}%) failed and {PASSED} ({PASSED * 100 // TOTAL}%) passed out of {TOTAL}")