from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional
from bson import ObjectId
from bson.errors import InvalidId 

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue

class PyObjectId(str):
    @classmethod
    def __get_pydantic_json_schema__(
        cls, core_schema: dict, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        return {"type": "string", "format": "objectid"}

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, *args):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            try:
                ObjectId(v)
                return v
            except InvalidId:
                pass
        raise ValueError("Invalid ObjectId")

from pydantic import field_validator


# Add this to all your models that need MongoDB _id
class MongoBaseModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        use_enum_values=True  # Add this to return enum values instead of enum objects
    )

class Status(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"

class StatusUpdate(BaseModel):
    status: Status
    time: Optional[str] = None  # Format: "HH:MM"

    @field_validator('time')
    def validate_time_format(cls, v):
        if v:
            try:
                hours, minutes = map(int, v.split(':'))
                if not (0 <= hours < 24 and 0 <= minutes < 60):
                    raise ValueError
            except ValueError:
                raise ValueError("Invalid time format. Use HH:MM")
        return v
class Relationship(str, Enum):
    SELF = "Self"
    FATHER = "Father"
    MOTHER = "Mother"
    SON = "Son"
    SPOUSE = "Spouse"
    DAUGHTER = "Daughter"
    FRIEND = "Friend"
    OTHER = "Other"

class Preference(str, Enum):
    ONLINE = "Online"
    OFFLINE = "Offline"

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

# Add to existing imports
class MaritalStatus(str, Enum):
    MARRIED = "Married"
    UNMARRIED = "Unmarried"

class Appointment(MongoBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    age: int
    date: datetime
    trainer: str
    gender: Gender
    mobile: str
    reason: str
    relationship: Relationship = Relationship.SELF
    marital_status: MaritalStatus
    preference: Preference
    status: Status = Status.PENDING

class AppointmentUpdate(MongoBaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    date: Optional[datetime] = None
    trainer: Optional[str] = None
    gender: Optional[Gender] = None
    mobile: Optional[str] = None
    reason: Optional[str] = None
    relationship: Optional[Relationship] = None
    marital_status: Optional[MaritalStatus] = None
    preference: Optional[Preference] = None
    status: Optional[Status] = None