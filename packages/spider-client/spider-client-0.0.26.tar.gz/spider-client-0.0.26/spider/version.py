import os

def get_version():
    version_file_path = os.path.join(os.path.dirname(__file__), "..", "VERSION")
    with open(version_file_path, "r", encoding="utf-8") as version_file:
        return version_file.read().strip()

__version__ = get_version()