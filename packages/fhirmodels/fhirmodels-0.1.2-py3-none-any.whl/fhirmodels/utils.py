import json
import mimetypes
import os
import typing as _t

from fhirmodels import constants as _c


def walk_directory(directory: str) -> _t.Iterator[str]:
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            yield os.path.join(root, filename)


def read_json_file(file_path: str) -> _t.Any:
    with open(file_path) as f:
        return json.load(f)


def is_json_file(file_path: str) -> bool:
    return mimetypes.guess_type(file_path)[0] == "application/json"


def is_choice_path(path: str):
    return "[x]" in path


def replace_choice_string(path: str, replace: str):
    return path.replace("[x]", replace)


def get_nth_part(path: str, n: int):
    return path.split(".")[n]


def remove_n_parts_from_start(path: str, n: int):
    return ".".join(path.split(".")[n:])


def remove_n_parts_from_end(path: str, n: int):
    return ".".join(path.split(".")[:-n])


def get_path_length(path: str):
    return len(path.split("."))


def is_root_path(path: str):
    if not path:
        return False
    return "." not in path


def join_paths(*paths: str):
    return ".".join(paths)


def get_python_type_for_primitive(fhir_type: str) -> type:
    """Returns the Python type for a FHIR primitive type."""
    if fhir_type in _c.FHIR_PRIMITIVES_TO_PYTHON_MAP:
        return _c.FHIR_PRIMITIVES_TO_PYTHON_MAP[fhir_type]
    elif fhir_type in _c.FHIR_PRIMITIVE_EXPANSION_MAP:
        return _c.FHIR_PRIMITIVES_TO_PYTHON_MAP[
            _c.FHIR_PRIMITIVE_EXPANSION_MAP[fhir_type]
        ]
    else:
        print("Unknown FHIR primitive type: %s", fhir_type)
        return str


def is_primitive_type(fhir_type: str) -> bool:
    """Returns True if the given FHIR type is a primitive type."""
    if fhir_type in _c.FHIR_PRIMITIVES_TO_PYTHON_MAP:
        return True
    elif fhir_type in _c.FHIR_PRIMITIVE_EXPANSION_MAP:
        return True
    else:
        return False
