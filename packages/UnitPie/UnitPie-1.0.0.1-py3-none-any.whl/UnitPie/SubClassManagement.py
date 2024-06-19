TestCases = []

class TestCase:
    def __init__(self, name):
        global TestCases
        self.name = name
        TestCases.append(self)

def GetTestCases() -> list[TestCase]:
    global TestCases
    return TestCases