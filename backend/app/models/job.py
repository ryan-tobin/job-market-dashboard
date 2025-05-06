from pydantic import BaseModel
from typing import List

class Job(BaseModel):
    title: str
    company: str
    location: str
    tags: List[str]

    model_config = {
        "from_attributes": True
    }