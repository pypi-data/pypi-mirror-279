from collections.abc import Sequence
from dataclasses import dataclass
from json import load
from pathlib import Path
from typing import TypeVar, NewType, Generic
from uuid import uuid4

Position = TypeVar('Position')
DataType = TypeVar('DataType')
InputID = NewType('InputID', str)


def parse_input_id(value: int | str | None) -> InputID:
    """
    Parses the input ID.

    Args:
        value: The input value to parse. Can be an integer, string, or None.

    Returns:
        An instance of the InputID class representing the parsed input ID. If value is None
        a random unique InputID will be generated.
    """
    if value is None:
        return InputID(str(uuid4()))
    else:
        return InputID(str(value))


@dataclass(frozen=True)
class InputData(Generic[DataType]):
    """
    InputData is a generic class that represents input data with a specific data type.

    Attributes:
    - id: An instance of InputID class that represents the unique identifier for the input data.
    - fields: A dictionary that contains the fields of the input data, where the keys are field names and the values are
     of the specified data type.


    Note: The class is decorated with the @dataclass(frozen=True) decorator to make it immutable.
    """
    id: InputID
    fields: dict[str, DataType]

    @classmethod
    def parse(cls, fields: dict[str, DataType], id_: str | int | None = None) -> 'InputData[DataType]':
        """
        Args:
            fields: A dictionary representing the input fields with keys as strings and values as the data types of each
            field.
            id_: An optional parameter indicating the input data ID. It can be a string, an integer, or None if no ID is
            provided.

        Returns:
            An instance of the 'InputData' class with the provided 'fields' dictionary and 'id_' as the input data ID.

        Example usage:
            fields = {'name': str, 'age': int, 'email': str}
            id_ = 12345
            input_data = MyClass.parse(fields, id_)
        """
        return cls(parse_input_id(id_), fields)

    @classmethod
    def from_json(cls, json_file: Path) -> Sequence['InputData[DataType]']:
        """
        Args:
            json_file: The path to the JSON file containing the data.

        Returns:
            A sequence of 'InputData[DataType]' objects, obtained by parsing the entries in the JSON file.

        Raises:
            FileNotFoundError: If the specified JSON file does not exist.

        Example:
            >>> json_path = Path('data.json')
            >>> data = InputData.from_json(json_path)

        """
        with json_file.open(encoding='utf-8') as src:
            return [
                cls.parse(entry, entry.get('id', i))
                for i, entry in enumerate(load(src))
            ]
