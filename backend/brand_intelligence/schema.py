

REQUIRED_SCHEMA = {
    "brand_voice": str,
    "core_emotions": list,
    "target_audience": dict,
    "communication_style": str,
    "cta_style": str
}
def validate_brand_output(data: dict):
    if not isinstance(data, dict):
        raise ValueError("Output is not a dictionary")

    for field, field_type in REQUIRED_SCHEMA.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

        if not isinstance(data[field], field_type):
            raise TypeError(
                f"Field '{field}' must be of type {field_type.__name__}"
            )

    return True

