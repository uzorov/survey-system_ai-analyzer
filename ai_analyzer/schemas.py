from typing import Optional
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    text: str


class AnalyzeResponse(BaseModel):
    type_of_pipe: Optional[str]
    diameter_of_pipe: Optional[str]
    pipe_wall_thickness: Optional[str]
    volume_tons: Optional[str]
    timeline: Optional[str]
    interest_level: Optional[str]
