from message import Message
from flag_bearer import FlagBearer
from parser import Parser
from util import output_vwap


class S(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, event_code):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.event_code = event_code

    def register(self):
        if self.event_code.decode('ascii') == 'O':
            print("Start of Messages")
            FlagBearer.prev_time = (int.from_bytes(self.timestamp, byteorder='big') // 1000000000) * 1000000000
            FlagBearer.taking_messages = True
        elif self.event_code.decode('ascii') == 'S':
            print("Start of System hours")
            FlagBearer.taking_orders = True
        elif self.event_code.decode('ascii') == 'Q':
            print("Start of Market hours")
            curr_time = int.from_bytes(self.timestamp, byteorder='big')
            FlagBearer.executing = True
            output_vwap(Parser.executed_orders, Parser.stock_names, curr_time)
        elif self.event_code.decode('ascii') == 'M':
            print("End of Market hours")
            curr_time = int.from_bytes(self.timestamp, byteorder='big')
            FlagBearer.executing = False
            output_vwap(Parser.executed_orders, Parser.stock_names, curr_time)
        elif self.event_code.decode('ascii') == 'E':
            print("End of System hours")
            FlagBearer.taking_orders = False
        elif self.event_code.decode('ascii') == 'C':
            print("End of Messages")
            FlagBearer.taking_messages = False
            exit()
        super().register()


class R(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, market_category, financial_status_indicator,
                 round_lot_size, round_lots_only, issue_classification, issue_sub_type, authenticity,
                 short_sale_threshold_indicator, ipo_flag, luld_reference_price_tier, etp_flag, etp_leverage_factor,
                 inverse_indicator):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.market_category = market_category
        self.financial_status_indicator = financial_status_indicator
        self.timestamp = timestamp
        self.round_lot_size = round_lot_size
        self.round_lots_only = round_lots_only
        self.issue_classification = issue_classification
        self.issue_sub_type = issue_sub_type
        self.authenticity = authenticity
        self.short_sale_threshold_indicator = short_sale_threshold_indicator
        self.ipo_flag = ipo_flag
        self.luld_reference_price_tier = luld_reference_price_tier
        self.etp_flag = etp_flag
        self.etp_leverage_factor = etp_leverage_factor
        self.inverse_indicator = inverse_indicator

    def register(self):
        Parser.stock_directory_message(self)
        super().register()


class H(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, trading_state, reserved, reason):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.trading_state = trading_state
        self.reserved = reserved
        self.reason = reason

    def register(self):
        super().register()


class Y(Message):
    def __init__(self, locate_code, tracking_number, timestamp, stock, reg_sho_action):
        self.locate_code = locate_code
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.reg_sho_action = reg_sho_action

    def register(self):
        super().register()


class L(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, mpid, stock, primary_market_maker, market_maker_mode,
                 market_participant_state):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.mpid = mpid
        self.stock = stock
        self.primary_market_maker = primary_market_maker
        self.market_maker_mode = market_maker_mode
        self.market_participant_state = market_participant_state

    def register(self):
        super().register()


class V(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, level_1, level_2, level_3):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3

    def register(self):
        super().register()


class W(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, breached_level):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.breached_level = breached_level

    def register(self):
        super().register()


class K(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, ipo_quotation_release_time,
                 ipo_quotation_release_qualifier, ipo_price):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.ipo_quotation_release_time = ipo_quotation_release_time
        self.ipo_quotation_release_qualifier = ipo_quotation_release_qualifier
        self.ipo_price = ipo_price

    def register(self):
        super().register()


class J(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, auction_collar_reference_price,
                 upper_auction_collar_price, lower_auction_collar_price, auction_collar_extension):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.auction_collar_reference_price = auction_collar_reference_price
        self.upper_auction_collar_price = upper_auction_collar_price
        self.lower_auction_collar_price = lower_auction_collar_price
        self.auction_collar_extension = auction_collar_extension

    def register(self):
        super().register()


class h(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, market_code, operation_halt_action):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.market_code = market_code
        self.operation_halt_action = operation_halt_action

    def register(self):
        super().register()


class A(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, buy_sell_indicator,
                 shares, stock, price):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.buy_sell_indicator = buy_sell_indicator
        self.shares = shares
        self.stock = stock
        self.price = price

    def register(self):
        if self.buy_sell_indicator.decode('ascii') == 'B':
            if FlagBearer.taking_orders:
                Parser.add_order_no_mpid(self)
        super().register()


class F(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, buy_sell_indicator,
                 shares, stock, price, attribution):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.buy_sell_indicator = buy_sell_indicator
        self.shares = shares
        self.stock = stock
        self.price = price
        self.attribution = attribution

    def register(self):
        if self.buy_sell_indicator.decode('ascii') == 'B':
            if FlagBearer.taking_orders:
                Parser.add_order_no_mpid(self)
        super().register()


class E(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, executed_shares, match_number):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.executed_shares = executed_shares
        self.match_number = match_number

    def register(self):
        if FlagBearer.executing:
            Parser.order_executed_message(self)
        super().register()


class C(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, executed_shares, match_number,
                 printable, execution_price):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.executed_shares = executed_shares
        self.match_number = match_number
        self.printable = printable
        self.execution_price = execution_price

    def register(self):
        if not self.printable.decode('ascii') == 'N':
            if FlagBearer.executing:
                Parser.order_executed_price_message(self)
        super().register()


class X(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, cancelled_shares):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.cancelled_shares = cancelled_shares

    def register(self):
        Parser.order_cancel_message(self)
        super().register()


class D(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number

    def register(self):
        Parser.order_delete_message(self)
        super().register()


class U(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, original_order_reference_number,
                 new_order_reference_number, shares, price):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.original_order_reference_number = original_order_reference_number
        self.new_order_reference_number = new_order_reference_number
        self.shares = shares
        self.price = price

    def register(self):
        Parser.order_replace_message(self)
        super().register()


class P(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, order_reference_number, buy_sell_indicator, shares,
                 stock, price, match_number):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.order_reference_number = order_reference_number
        self.buy_sell_indicator = buy_sell_indicator
        self.shares = shares
        self.stock = stock
        self.price = price
        self.match_number = match_number

    def register(self):
        if self.buy_sell_indicator.decode('ascii') == 'B':
            Parser.trade_message(self)
        super().register()


class Q(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, shares, stock, cross_price, match_number, cross_type):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.shares = shares
        self.stock = stock
        self.cross_price = cross_price
        self.match_number = match_number
        self.cross_type = cross_type

    def register(self):
        Parser.cross_trade_message(self)
        super().register()


class B(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, match_number):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.match_number = match_number

    def register(self):
        Parser.broken_trade_execution_message(self)
        super().register()


class I(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, paired_shares, imbalance_shares, imbalance_direction,
                 stock, far_price, near_price, current_reference_price, cross_type, price_variation_indicator):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.paired_shares = paired_shares
        self.imbalance_shares = imbalance_shares
        self.imbalance_direction = imbalance_direction
        self.stock = stock
        self.far_price = far_price
        self.near_price = near_price
        self.current_reference_price = current_reference_price
        self.cross_type = cross_type
        self.price_variation_indicator = price_variation_indicator

    def register(self):
        super().register()


class N(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, stock, interest_flag):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.interest_flag = interest_flag

    def register(self):
        super().register()


class O(Message):
    def __init__(self, stock_locate, tracking_number, timestamp, open_eligibility_status, stock,
                 minimum_allowable_price, maximum_allowable_price, near_execution_price, near_execution_time,
                 lower_price_range_collar, upper_price_range_collar):
        self.stock_locate = stock_locate
        self.tracking_number = tracking_number
        self.timestamp = timestamp
        self.stock = stock
        self.open_eligibility_status = open_eligibility_status
        self.minimum_allowable_price = minimum_allowable_price
        self.maximum_allowable_price = maximum_allowable_price
        self.near_execution_price = near_execution_price
        self.near_execution_time = near_execution_time
        self.lower_price_range_collar = lower_price_range_collar
        self.upper_price_range_collar = upper_price_range_collar

    def register(self):
        super().register()
