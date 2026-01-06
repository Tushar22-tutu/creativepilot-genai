import json
import os

MEMORY_FILE = "brand_memory.json"
BRAND_MEMORY = {}


def load_memory_from_file():
    global BRAND_MEMORY

    if not os.path.exists(MEMORY_FILE):
        BRAND_MEMORY = {}
        return

    with open(MEMORY_FILE, "r") as f:
        try:
            BRAND_MEMORY = json.load(f)
        except json.JSONDecodeError:
            BRAND_MEMORY = {}


def save_memory_to_file():
    with open(MEMORY_FILE, "w") as f:
        json.dump(BRAND_MEMORY, f, indent=2)


def get_brand_from_memory(brand_name: str):
    return BRAND_MEMORY.get(brand_name)


def save_brand_to_memory(brand_name: str, brand_profile: dict):
    BRAND_MEMORY[brand_name] = brand_profile
    save_memory_to_file()
