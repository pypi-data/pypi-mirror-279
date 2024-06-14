from dataclasses import dataclass
from typing import Optional

from .identified import Identified


@dataclass
class KeyringSummary(Identified):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
