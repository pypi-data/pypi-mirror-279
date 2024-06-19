from pydantic import BaseModel, ConfigDict

class SheetMeta(BaseModel):
  model_config = ConfigDict(extra='allow')
  model: str | None = None
