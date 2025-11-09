from dataclasses import dataclass
import enum


class TokenType(enum.Enum):
    ACCESS = 'access'
    REFRESH = 'refresh'

@dataclass
class TokenPair:
    access_token: str
    refresh_token: str