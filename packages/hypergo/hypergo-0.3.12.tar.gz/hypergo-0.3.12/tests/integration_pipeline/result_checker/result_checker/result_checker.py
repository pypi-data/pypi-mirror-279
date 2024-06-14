from typing import Any, Dict


def check_results(
    result: Any = None,
    expected_result: Any = None
) -> None:
    if result != expected_result:
        raise Exception(f"Result does not match the expected result.\nResult: {result}\nExpected: {expected_result}")


if __name__ == "__main__":
    print(check_results({"im": "right"}, {"im": "right"}))
    print(check_results({"im": "wrong"}, {"im": "right"}))
