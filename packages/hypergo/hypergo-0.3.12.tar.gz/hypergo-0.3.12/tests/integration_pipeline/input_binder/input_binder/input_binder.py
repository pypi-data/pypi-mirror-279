from typing import Any, Dict


def bind_inputs(
    first_level_input: Any = None,
    custom_property_input: Any = None,
    structured_input_data: Any = None
) -> Dict[str, Any]:
    return {
        "first_level_input": first_level_input,
        "custom_property_input": custom_property_input,
        "structured_input_data": structured_input_data
    }


if __name__ == "__main__":
    print(bind_inputs("first_level_input", "custom_property_input", {"structured_input_data": "structured_input_data"}))
