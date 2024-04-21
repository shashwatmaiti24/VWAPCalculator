class Parser:
    buy_orders = dict()
    stock_names = dict()
    executed_orders = dict()
    vwap = dict()

    @staticmethod
    def stock_directory_message(message):
        stock_name = message.stock.decode('ascii', 'ignore').strip()
        Parser.stock_names[message.stock_locate] = stock_name
        Parser.executed_orders[message.stock_locate] = []

    @staticmethod
    def add_order_no_mpid(message):
        Parser.buy_orders[message.order_reference_number] = [message.price / 10000, message.shares,
                                                             message.stock_locate]

    @staticmethod
    def order_executed_message(message):
        timestamp = int.from_bytes(message.timestamp, byteorder='big')
        if Parser.buy_orders.get(message.order_reference_number):
            price, qty_, _ = Parser.buy_orders.get(message.order_reference_number)
            if qty_ > message.executed_shares:
                Parser.buy_orders.update(
                    {message.order_reference_number: [price, qty_ - message.executed_shares, message.stock_locate]})
            else:
                del Parser.buy_orders[message.order_reference_number]
            Parser.executed_orders[message.stock_locate].append(
                [price, message.executed_shares, 0, message.match_number, timestamp])

        else:
            return

    @staticmethod
    def order_executed_price_message(message):
        timestamp = int.from_bytes(message.timestamp, byteorder='big')
        if Parser.buy_orders.get(message.order_reference_number):
            price_, qty_, _ = Parser.buy_orders.get(message.order_reference_number)
            if qty_ > message.executed_shares:
                Parser.buy_orders.update(
                    {message.order_reference_number: [price_, qty_ - message.executed_shares, message.stock_locate]})
            else:
                del Parser.buy_orders[message.order_reference_number]
            Parser.executed_orders[message.stock_locate].append(
                [message.execution_price / 10000, message.executed_shares, 0, message.match_number, timestamp])
        else:
            return

    @staticmethod
    def order_cancel_message(message):
        if Parser.buy_orders.get(message.order_reference_number):
            Parser.buy_orders[message.order_reference_number][1] = Parser.buy_orders[message.order_reference_number][
                                                                     1] - message.cancelled_shares
            if Parser.buy_orders[message.order_reference_number][1] <= 0:
                del Parser.buy_orders[message.order_reference_number]
        else:
            return

    @staticmethod
    def order_delete_message(message):
        Parser.buy_orders.pop(message.order_reference_number, None)

    @staticmethod
    def order_replace_message(message):
        Parser.buy_orders.pop(message.original_order_reference_number, None)
        Parser.buy_orders[message.new_order_reference_number] = [message.price / 10000, message.shares,
                                                               message.stock_locate]

    @staticmethod
    def trade_message(message):
        timestamp = int.from_bytes(message.timestamp, byteorder='big')
        Parser.executed_orders[message.stock_locate].append(
            [message.price / 10000, message.shares, 0, message.match_number, timestamp])

    @staticmethod
    def cross_trade_message(message):
        timestamp = int.from_bytes(message.timestamp, byteorder='big')
        Parser.executed_orders[message.stock_locate].append(
            [message.cross_price / 10000, message.shares, 0, message.match_number, timestamp])

    @staticmethod
    def broken_trade_execution_message(message):
        if Parser.executed_orders.get(message.stock_locate):
            orders = Parser.executed_orders.get(message.stock_locate)
            if orders is not None:
                new_orders = list(filter(lambda a: not a[3] == message.match_number, orders))
                Parser.executed_orders.update({message.stock_locate: new_orders})
        else:
            return
