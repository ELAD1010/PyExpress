from enum import Enum

from httper.common.inet.layers.l7 import HTTP
from httper.common.inet.layers.l4 import TCP, UDP
from httper.common.inet.layers.l3 import IP


class Layers(Enum):
    TCP: TCP
    UDP: UDP
    IP: IP
    HTTP: HTTP


