from datetime import date, datetime, time, timezone
from typing import Annotated, Any, Dict, Generic, List, TypeVar

from bson import ObjectId
from pydantic import BaseModel, ConfigDict
from pydantic.functional_serializers import PlainSerializer

from fa_common.utils import sizeof_fmt

MT = TypeVar("MT")


def camel_case(string: str) -> str:
    assert isinstance(string, str), "Input must be of type str"

    first_alphabetic_character_index = -1
    for index, character in enumerate(string):
        if character.isalpha():
            first_alphabetic_character_index = index
            break

    empty = ""

    if first_alphabetic_character_index == -1:
        return empty

    string = string[first_alphabetic_character_index:]

    titled_string_generator = (character for character in string.title() if character.isalnum())

    try:
        return next(titled_string_generator).lower() + empty.join(titled_string_generator)

    except StopIteration:
        return empty


def to_camel(string):
    if string == "id":
        return "_id"
    if string.startswith("_"):  # "_id"
        return string
    return camel_case(string)


DatetimeType = Annotated[
    datetime,
    PlainSerializer(
        lambda dt: dt.replace(microsecond=0, tzinfo=timezone.utc).isoformat(),
        return_type=str,
        when_used="json",
    ),
]
DateType = Annotated[date, PlainSerializer(lambda dt: dt.isoformat(), return_type=str, when_used="json")]
TimeType = Annotated[
    time,
    PlainSerializer(
        lambda dt: dt.replace(microsecond=0, tzinfo=timezone.utc).isoformat(),
        return_type=str,
        when_used="json",
    ),
]
ObjectIdType = Annotated[ObjectId, PlainSerializer(lambda oid: str(oid), return_type=str, when_used="json")]


class CamelModel(BaseModel):
    """
    Replacement for pydanitc BaseModel which simply adds a camel case alias to every field
    NOTE: This has been updated for Pydantic 2 to remove some common encoding helpers
    """

    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class File(CamelModel):
    size: str | None = None  # e.g. '3 KB'
    size_bytes: int | None = None
    url: str | None = None  # download url
    gs_uri: str | None = None  # GSC Uri
    id: str | None = None  # id can be path or database id
    dir: bool = False
    path: str | None = None  # path to current item (e.g. /folder1/someFile.txt)
    # optional (but we are using id as name if name is not present) (e.g. someFile.txt)
    name: str
    content_type: str | None = None

    def set_size(self, bytes: int):  # noqa: A002
        self.size = sizeof_fmt(bytes)
        self.size_bytes = bytes


class FileDownloadRef(CamelModel):
    name: str
    url: str
    extension: str
    size: int


class Message(CamelModel):
    message: str = ""
    warnings: List[str] | None = None


class MessageValue(Message, Generic[MT]):
    return_value: MT | None = None


class MessageValueList(Message):
    return_value: List[str]


class MessageValueFiles(Message):
    return_value: List[File]


class ErrorResponse(CamelModel):
    code: str | None = None
    detail: str | None = None
    fields: List[Dict[str, Any]] | None = None
    error: str | None = None
    errors: List[Dict[str, Any]] = []
    trace: str | None = None


class Version(CamelModel):
    version: str
    commit_id: str | None = None
    build_date: datetime | str | None = None
    framework_version: str | None = None
