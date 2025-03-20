from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union, Optional

class Post(BaseModel):
    title: str = Field(min_length=2)
    description: str = Field(min_length=5)
    author: str = Field(min_length=2)
    is_moderated: bool = Field(default=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=None)
    # updated_at: Union[datetime, None] = None  # gleich wie oben
    # updated_at: Optional[datetime] = None

    class Config:
        str_strip_whitespace = True
        validate_assignment = True

nachricht = Post(
    title="Nachricht",
    description="Sportsnachricht",
    author="Alex Green",
    is_moderated=True,
    created_at=datetime.now()
)

print(nachricht.model_dump_json())