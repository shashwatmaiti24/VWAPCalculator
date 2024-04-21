from flag_bearer import FlagBearer
from parser import Parser
from util import output_vwap

class Message:
    def register(self):
        curr_time = int.from_bytes(self.timestamp, byteorder='big')
        if curr_time - FlagBearer.prev_time >= FlagBearer.HOUR:
            output_vwap(Parser.executed_orders, Parser.stock_names, curr_time)
