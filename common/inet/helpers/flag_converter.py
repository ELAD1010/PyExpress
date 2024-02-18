from enum import Enum

class Flags(int, Enum):
    SYN = 2,
    ACK = 16,
    SYN_ACK = 18
    FIN_ACK = 17
    RST_ACK = 20
    PSH_ACK = 24
    FIN_PSH_ACK = 25
    CONGESTION = 194


FLAGS = {Flags.SYN: 'SYN', Flags.ACK: 'ACK',  Flags.SYN_ACK: 'SYN-ACK', Flags.PSH_ACK: 'PSH-ACK', Flags.FIN_ACK: 'FIN-ACK',
         Flags.RST_ACK: 'RST-ACK', Flags.FIN_PSH_ACK: 'FIN-PSH-ACK', Flags.CONGESTION: 'Congestion Window Reduced'}

