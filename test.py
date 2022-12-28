from functions import perform

def test(val, expect) -> str:
    if run(val, expect):
        return "PASSED"
    else:
        return f"ERROR. Expected: {expect}, got {perform(val)}"

def run(val, expect) -> bool:
    return expect == perform(val)
    

print(test("Скyпаю пушkинckие kарты", "скупаю пушкинские карты"))
# print(test("ПуWкинcкая", "пушкинская"))
# print(test("Здар0ва", "здарова"))
# print(test("Tесt", "тест"))