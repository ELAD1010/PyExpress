from enum import Enum

class PduType(str, Enum):
    SynSegment = 'Syn'
    HttpRequest = 'HttpRequest'
    