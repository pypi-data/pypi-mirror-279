from importlib import import_module

from fhirmodels import utils


class FhirBaseModel:
    """Base class for all generated models."""

    property_class_info = {}

    def __init__(self):
        pass

    @classmethod
    def from_dict(cls, data: dict):
        """Create a model instance from a dict. The instance is recursively
        created by importing the classes for complex FHIR types."""
        instance = cls()
        models_path = utils.remove_n_parts_from_end(cls.__module__, 1)

        def handle_dict_value(key: str, value: dict):
            # Capitalize the class name if it's not
            if key not in cls.property_class_info:
                setattr(instance, key, value)
                return
            class_name = instance.property_class_info[key]["class_name"]
            is_contained = cls.property_class_info[key]["is_contained"]
            if is_contained:
                module = import_module(cls.__module__)
                model_class = getattr(module, class_name)
            else:
                import_path = f"{models_path}.{class_name}"
                module = import_module(import_path)
                model_class = getattr(module, class_name)
            nested_instance = model_class.from_dict(value)
            return nested_instance

        for key, value in data.items():
            if isinstance(value, dict):  # complex type
                nested_instance = handle_dict_value(key, value)
                setattr(instance, key, nested_instance)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):  # complex type
                        # mutating mutable object no need to reassign
                        if key not in cls.property_class_info:
                            if hasattr(instance, key):
                                getattr(instance, key).append(item)
                            else:
                                setattr(instance, key, [item])
                            continue
                        nested_instance = handle_dict_value(key, item)
                        getattr(instance, key).append(nested_instance)
                    else:  # primitive type
                        getattr(instance, key).append(item)
            else:  # primitive type
                setattr(instance, key, value)

        return instance

    @classmethod
    def from_obj(cls, data):
        """Creates a model instance from an object or a dictionary."""
        if isinstance(data, dict):
            return cls.from_dict(data)
        elif hasattr(data, "as_dict") and callable(data.as_dict):
            return cls.from_dict(data.as_dict())
        else:
            raise ValueError(
                "Invalid input object. Must be a dictionary or an object with an 'as_dict' method."
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.as_dict()})"

    def as_dict(self):
        # from https://stackoverflow.com/questions/7963762/what-is-the-most-economical-way-to-convert-nested-python-objects-to-dictionaries
        def serialize(obj):
            if isinstance(obj, FhirBaseModel):
                return obj.as_dict()
            elif isinstance(obj, (list, tuple)):
                return [serialize(item) for item in obj]
            elif isinstance(obj, dict):
                return {
                    key: serialize(value)
                    for key, value in obj.items()
                    if value is not None and value != []
                }
            else:
                return obj  # Handle basic types

        return {
            key: serialize(value)
            for key, value in self.__dict__.items()
            if value is not None and value != []
        }
