from pydantic import ConfigDict
from moveread.labels import Annotations as PlayerAnnotations, Styles, StylesNA, Language

class PlayerMeta(PlayerAnnotations):
  model_config = ConfigDict(extra='allow')
