# Simple in-memory brand memory

BRAND_MEMORY = {}


def get_brand_from_memory(brand_name: str):
    return BRAND_MEMORY.get(brand_name)


def save_brand_to_memory(brand_name: str, brand_profile: dict):
    BRAND_MEMORY[brand_name] = brand_profile
