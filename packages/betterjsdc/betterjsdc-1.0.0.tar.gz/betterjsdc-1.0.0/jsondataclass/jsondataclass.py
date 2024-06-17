from types import NoneType, UnionType, GenericAlias
import json
from typing import NewType, TypeVar, Optional, get_origin, get_args, overload, Literal, Union
from dataclasses import dataclass, field, fields, is_dataclass, _MISSING_TYPE, Field
from enum import Enum

DataClassType = TypeVar('DataClassType', bound=dataclass)
TypeType = TypeVar('TypeType', bound=type)
Generic = TypeVar('Generic', covariant=True)
def is_json_serializable(value: any) -> bool:
    try:
        json.dumps(value)
        return True
    except Exception:
        return False

@dataclass
class DataField:
    field_name: str | None
    field_type: TypeType
    in_list: bool = False

    def __repr__(self) -> str:
        return f"{self.field_name}: {self.field_type}"
    
    def __str__(self) -> str:
        return self.__repr__()


def does_field_have_default(_field: Field):
    return not isinstance(_field.default, _MISSING_TYPE) or not isinstance(_field.default_factory, _MISSING_TYPE)


def desearialize_field(field_type: type[Generic] | GenericAlias | UnionType, field_value: Generic, field_metadata: dict) -> tuple[Generic | list[Generic], list[DataField]]:
    if (deserializer := field_metadata.get("deserializer", False)):
        field_value = deserializer(field_value)

    if isinstance(field_type, UnionType) or get_origin(field_type) == Union:
        if NoneType in get_args(field_type):
            if field_value is None:
                return None, []
        for union_type in get_args(field_type):
            if union_type is NoneType:
                continue
            try:
                data, missing_items = desearialize_field(union_type, field_value, field_metadata)
                if len(missing_items) > 0:
                    continue
                return data, missing_items
            except Exception as e:
                continue
        raise ValueError(f"Could not deserialize {field_value} to any of the types in {field_type}")

    if isinstance(field_type, type):
        if issubclass(field_type, NewType):
            field_type = field_type.__supertype__

    if is_dataclass(field_type) and isinstance(field_value, dict):
        return dict_to_dataclass(field_type, field_value, True)
    elif isinstance(field_value,list) and isinstance(field_type, GenericAlias) and issubclass(get_origin(field_type), list):
        data = [desearialize_field(get_args(field_type)[0], item, {}) for item in field_value]
        missing_items = []
        for i, item in enumerate(data):
            for missing_item in item[1]:
                missing_items.append(DataField(field_name=f"[{i}].{missing_item.field_name}" if missing_item.field_name else f"[{i}]", field_type=missing_item.field_type, in_list=True))
        return [item[0] for item in data], missing_items
    elif isinstance(field_value, dict) and isinstance(field_type, GenericAlias) and issubclass(get_origin(field_type), dict):
        data = {key: desearialize_field(get_args(field_type)[1], value, {}) for key, value in field_value.items()}
        keys = {key: desearialize_field(get_args(field_type)[0], key, {}) for key in data.keys()}
        missing_items = []
        for key, value in data.items():
            for missing_item in value[1]:
                missing_items.append(DataField(field_name=f"[{key}].{missing_item.field_name}" if missing_item.field_name else f"[{key}]", field_type=missing_item.field_type, in_list=True))
        for keys_key, key in keys.items():
            for missing_item in key[1]:
                missing_items.append(DataField(field_name=f"[<{keys_key}.{missing_item.field_name}>]" if missing_item.field_name else f"[<{keys_key}>]", field_type=missing_item.field_type, in_list=True))
        return {keys[key][0]: value[0] for key, value in data.items()}, missing_items
    elif isinstance(field_value, list) and isinstance(field_type, GenericAlias) and issubclass(get_origin(field_type), set):
        data = [desearialize_field(get_args(field_type)[0], item, {}) for item in field_value]
        missing_items = []
        for i, item in enumerate(data):
            for missing_item in item[1]:
                missing_items.append(DataField(field_name=f"[{i}].{missing_item.field_name}" if missing_item.field_name else f"[{i}]", field_type=missing_item.field_type, in_list=True))
        return set([item[0] for item in data]), missing_items    
    elif isinstance(field_value, (tuple, list)) and isinstance(field_type, GenericAlias) and issubclass(get_origin(field_type), tuple):
        data = [desearialize_field(get_args(field_type)[i], item, {}) for i, item in enumerate(field_value)]
        missing_items = []
        for i, item in enumerate(data):
            for missing_item in item[1]:
                missing_items.append(DataField(field_name=f"[{i}].{missing_item.field_name}" if missing_item.field_name else f"[{i}]", field_type=missing_item.field_type, in_list=True))
        return tuple([item[0] for item in data]), missing_items
    elif get_origin(field_type) == Literal:
        if field_value in get_args(field_type):
            return field_value, []
        else:
            raise ValueError(f"Value {field_value} not in {field_type}")
    elif isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(field_value), []
    elif not isinstance(field_value, field_type):
        if field_value is None or issubclass(field_type, str) or issubclass(field_type, bool):
            return None, [DataField(field_name=None, field_type=field_type)]
        return field_type.__new__(field_type, field_value), []
    else:
        return field_value, []

@overload
def dict_to_dataclass(dataclass_type: type[DataClassType], input_dict: dict, ret_missing: Literal[True]) -> tuple[DataClassType, list[DataField]]:
    ...

@overload
def dict_to_dataclass(dataclass_type: type[DataClassType], input_dict: dict, ret_missing: Literal[False]) -> DataClassType:
    ...

@overload
def dict_to_dataclass(dataclass_type: type[DataClassType], input_dict: dict) -> tuple[DataClassType, list[DataField]]:
    ...

def dict_to_dataclass(dataclass_type: type[DataClassType], input_dict: dict, ret_missing: bool = False) -> tuple[DataClassType, list[DataField]] | DataClassType:
    assert is_dataclass(dataclass_type), f"Expected dataclass, got {type(dataclass_type)}"

    init_params = {}
    missing_fields: list[DataField] = []

    for field in fields(dataclass_type):
        if not field.init:
            continue

        field_type = field.type
        field_metadata = field.metadata
        field_name: str = field_metadata.get("rename", field.name)

        if field.default is _MISSING_TYPE and field.default_factory is _MISSING_TYPE:
            if field_name not in input_dict:
                missing_fields.append(DataField(field_name=field_name, field_type=field.type))
                continue

        field_value = input_dict[field_name]

        try:
            data, missing_items_1 = desearialize_field(field_type, field_value, field_metadata)
            for missing_item in missing_items_1:
                if missing_item.field_name is not None:
                    missing_field_name = f"{field_name}.{missing_item.field_name}" if not missing_item.in_list else f"{field_name}{missing_item.field_name}"
                else:
                    missing_field_name = field_name
                missing_fields.append(DataField(field_name=missing_field_name, field_type=missing_item.field_type))

            init_params[field.name] = data

        except Exception as e:
            missing_fields.append(DataField(field_name=field_name, field_type=field.type))

    if len(missing_fields) > 0:
        if ret_missing:
            return None, missing_fields
        else:
            return None

    if ret_missing:
        return dataclass_type(**init_params), missing_fields
    else:
        return dataclass_type(**init_params)


def value_to_json_serializable(field_value: Generic, field_metadata: dict) -> any:
    if is_dataclass(field_value):
        return dataclass_to_dict(field_value)
    elif isinstance(field_value, tuple):
        return [value_to_json_serializable(item, {}) for item in field_value]
    elif isinstance(field_value, Enum):
        return field_value.value
    elif isinstance(field_value, list):
        return [value_to_json_serializable(item, {}) for item in field_value]
    elif is_json_serializable(field_value):
        return field_value
    elif isinstance(field_value, set):
        return [value_to_json_serializable(item, {}) for item in field_value]
    else:
        raise ValueError(f"Unsupported type {type(field_value)}")

def dataclass_to_dict(dataclass_instance: DataClassType) -> dict:
    assert is_dataclass(dataclass_instance), f"Expected dataclass, got {type(dataclass_instance)}"
    output_dict = {}

    for field in fields(dataclass_instance):


        field_type = field.type
        field_metadata = field.metadata
        field_name = field.metadata.get("rename", field.name)

        field_value = getattr(dataclass_instance, field.name)

        if (serializer := field_metadata.get("serializer", False)):
            field_value = serializer(field_value)
        
        if isinstance(field_type, NewType):
            field_type = field_type.__supertype__   

        if isinstance(field_value, dict):
            field_value = {key: dataclass_to_dict(value) if is_dataclass(value) else value for key, value in field_value.items()}

        try:
            output_dict[field_name] = value_to_json_serializable(field_value, field_metadata)
        except ValueError as e:
            raise ValueError(f"Unsupported type {type(field_value)} for field {field_name}")
        
    return output_dict

def dumps(dataclass_instance: DataClassType) -> str:
    return json.dumps(dataclass_to_dict(dataclass_instance))

def loads(dataclass_type: type[DataClassType], input_string: str) -> DataClassType:
    return dict_to_dataclass(dataclass_type, json.loads(input_string))

def dump(dataclass_instance: DataClassType, file: str) -> None:
    with open(file, "w") as f:
        f.write(dumps(dataclass_instance))
    
def load(dataclass_type: type[DataClassType], file: str) -> DataClassType:
    with open(file, "r") as f:
        return loads(dataclass_type, f.read())