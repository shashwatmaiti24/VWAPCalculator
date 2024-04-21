import os
from flag_bearer import FlagBearer
from parser import Parser

save_path = 'out/'
directory = os.path.dirname(save_path)
if not os.path.exists(directory):
    os.makedirs(directory)


def output_vwap(executed_orders, stock_names, curr_time):
    FlagBearer.prev_time = (curr_time // 1000000000) * 1000000000
    print('Time from midnight: ', str((FlagBearer.prev_time // 3.6e11) / 10), 'hours')
    for locate_id, trades in executed_orders.items():
        low = 0
        high = 0
        closeTime = 0
        close = 0
        volume = 0
        for trade in trades:
            if trade[0] > 0:
                if low > 0:
                    low = min(trade[0], low)
                else:
                    low = trade[0]
                if high > 0:
                    high = max(trade[0], high)
                else:
                    high = trade[0]
                close = trade[0] if closeTime < trade[3] else close
                closeTime = max(trade[3], closeTime)
                volume += trade[1]
        if stock_names.get(locate_id):
            if volume == 0:
                Parser.vwap[stock_names.get(locate_id)] = [0, 0, 0]
                continue
            if Parser.vwap.get(stock_names.get(locate_id)):
                prev = Parser.vwap.get(stock_names.get(locate_id))
                cv = prev[0] + volume
                ctpv = prev[1] + volume * (low + high + close) / 3
                vwap_hour = ctpv / cv
            else:
                cv = volume
                ctpv = volume * (low + high + close) / 3
                vwap_hour = ctpv / cv
            Parser.vwap[stock_names.get(locate_id)] = [cv, ctpv, vwap_hour]
    FlagBearer.executed_orders = dict()

    fout = save_path + str((FlagBearer.prev_time // 3.6e11) / 10) + ".txt"
    with open(fout, "w+") as fo:
        for k, v in Parser.vwap.items():
            fo.write(str(k) + ' ' + str(v[2]) + '\n')
