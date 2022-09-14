# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.ws.base.exchange import Exchange
from ccxt.rest.async_support import aax as aaxRest
from ccxt.ws.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import NotSupported


class aax(Exchange, aaxRest):

    def describe(self):
        return self.deep_extend(super(aax, self).describe(), {
            'has': {
                'ws': True,
                'watchOHLCV': True,
                'watchOrderBook': True,
                'watchTicker': True,
                'watchTrades': True,
                'watchBalance': True,
                'watchOrders': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://realtime.aax.com/marketdata/v2/',
                        'private': 'wss://stream.aax.com/notification/v2/',
                    },
                },
            },
            'options': {
                'OHLCVLimit': 1000,
                'tradesLimit': 1000,
                'ordersLimit': 1000,
                'myTradesLimit': 1000,
            },
        })

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        name = 'candles'
        market = self.market(symbol)
        interval = self.timeframes[timeframe]
        messageHash = market['id'] + '@' + interval + '_' + name
        url = self.urls['api']['ws']['public']
        subscribe = {
            'e': 'subscribe',
            'stream': messageHash,
        }
        request = self.deep_extend(subscribe, params)
        ohlcv = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #     {
        #         c: '53876.69000000',
        #         e: 'BTCUSDT@1m_candles',
        #         h: '53876.69000000',
        #         l: '53832.47000000',
        #         o: '53832.47000000',
        #         s: 1619707320,  # start
        #         t: 1619707346,  # end
        #         v: '301.70946400'
        #     }
        #
        messageHash = self.safe_string(message, 'e')
        parts = messageHash.split('@')
        marketId = self.safe_string(parts, 0)
        timeframeName = self.safe_string(parts, 1)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        parsed = [
            self.safe_timestamp(message, 's'),
            self.safe_number(message, 'o'),
            self.safe_number(message, 'h'),
            self.safe_number(message, 'l'),
            self.safe_number(message, 'c'),
            self.safe_number(message, 'v'),
        ]
        subParts = timeframeName.split('_')
        interval = self.safe_string(subParts, 0)
        timeframe = self.find_timeframe(interval)
        # TODO: move to base class
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        stored.append(parsed)
        client.resolve(stored, messageHash)

    async def watch_ticker(self, symbol, params={}):
        name = 'tickers'
        await self.load_markets()
        market = self.market(symbol)
        messageHash = market['id'] + '@' + name
        url = self.urls['api']['ws']['public']
        subscribe = {
            'e': 'subscribe',
            'stream': name,
        }
        request = self.extend(subscribe, params)
        return await self.watch(url, messageHash, request, name)

    def handle_tickers(self, client, message):
        #
        #     {
        #         e: 'tickers',
        #         t: 1619663715213,
        #         tickers: [
        #             {
        #                 a: '0.00000000',
        #                 c: '47655.65000000',
        #                 d: '-3.48578544',
        #                 h: '50451.37000000',
        #                 l: '47002.45000000',
        #                 o: '49376.82000000',
        #                 s: 'YFIUSDT',
        #                 v: '18140.31675687'
        #             },
        #             {
        #                 a: '0.00000000',
        #                 c: '1.39127000',
        #                 d: '-3.09668252',
        #                 h: '1.43603000',
        #                 l: '1.28451000',
        #                 o: '1.43573000',
        #                 s: 'XRPUSDT',
        #                 v: '451952.36683000'
        #             },
        #         ]
        #     }
        #
        name = self.safe_string(message, 'e')
        timestamp = self.safe_integer(message, 't')
        extension = {
            'timestamp': timestamp,
            'datetime': self.iso8601(timestamp),
        }
        tickers = self.parse_tickers(self.safe_value(message, 'tickers', []), None, extension)
        symbols = list(tickers.keys())
        for i in range(0, len(symbols)):
            symbol = symbols[i]
            if symbol in self.markets:
                market = self.market(symbol)
                ticker = tickers[symbol]
                self.tickers[symbol] = ticker
                messageHash = market['id'] + '@' + name
                client.resolve(ticker, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        name = 'trade'
        await self.load_markets()
        market = self.market(symbol)
        messageHash = market['id'] + '@' + name
        url = self.urls['api']['ws']['public']
        subscribe = {
            'e': 'subscribe',
            'stream': messageHash,
        }
        request = self.extend(subscribe, params)
        trades = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        #     {
        #         e: 'BTCUSDT@trade',
        #         p: '-54408.21000000',
        #         q: '0.007700',
        #         t: 1619644477710
        #     }
        #
        messageHash = self.safe_string(message, 'e')
        parts = messageHash.split('@')
        marketId = self.safe_string(parts, 0)
        market = self.safe_market(marketId)
        symbol = market['symbol']
        # timestamp = self.safe_integer(message, 't')
        # amount = self.safe_number(message, 'q')
        # price = self.safe_number(message, 'p')
        trade = self.parse_trade(message, market)
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        stored.append(trade)
        client.resolve(stored, messageHash)

    async def watch_order_book(self, symbol, limit=None, params={}):
        name = 'book'
        await self.load_markets()
        market = self.market(symbol)
        limit = 20 if (limit is None) else limit
        if (limit != 20) and (limit != 50):
            raise NotSupported(self.id + ' watchOrderBook() accepts limit values of 20 or 50 only')
        messageHash = market['id'] + '@' + name + '_' + str(limit)
        url = self.urls['api']['ws']['public']
        subscribe = {
            'e': 'subscribe',
            'stream': messageHash,
        }
        request = self.extend(subscribe, params)
        orderbook = await self.watch(url, messageHash, request, messageHash)
        return orderbook.limit(limit)

    def handle_delta(self, bookside, delta):
        price = self.safe_float(delta, 0)
        amount = self.safe_float(delta, 1)
        bookside.store(price, amount)

    def handle_deltas(self, bookside, deltas):
        for i in range(0, len(deltas)):
            self.handle_delta(bookside, deltas[i])

    def handle_order_book(self, client, message):
        #
        #     {
        #         asks: [
        #             ['54397.48000000', '0.002300'],
        #             ['54407.86000000', '1.880000'],
        #             ['54409.34000000', '0.046900'],
        #         ],
        #         bids: [
        #             ['54383.17000000', '1.380000'],
        #             ['54374.43000000', '1.880000'],
        #             ['54354.07000000', '0.013400'],
        #         ],
        #         e: 'BTCUSDT@book_20',
        #         t: 1619626148086
        #     }
        #
        messageHash = self.safe_string(message, 'e')
        marketId, nameLimit = messageHash.split('@')
        parts = nameLimit.split('_')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        limitString = self.safe_string(parts, 1)
        limit = int(limitString)
        timestamp = self.safe_integer(message, 't')
        snapshot = self.parse_order_book(message, symbol, timestamp)
        orderbook = None
        if not (symbol in self.orderbooks):
            orderbook = self.order_book(snapshot, limit)
            self.orderbooks[symbol] = orderbook
        else:
            orderbook = self.orderbooks[symbol]
            orderbook.reset(snapshot)
        client.resolve(orderbook, messageHash)

    def request_id(self):
        # their support said that reqid must be an int32, not documented
        reqid = self.sum(self.safe_integer(self.options, 'reqid', 0), 1)
        self.options['reqid'] = reqid
        return reqid

    async def handshake(self, params={}):
        url = self.urls['api']['ws']['private']
        client = self.client(url)
        event = 'handshake'
        future = client.future(event)
        authenticated = self.safe_value(client.subscriptions, event)
        if authenticated is None:
            requestId = self.request_id()
            query = {
                'event': '#' + event,
                'data': {},
                'cid': requestId,
            }
            request = self.extend(query, params)
            messageHash = str(requestId)
            response = await self.watch(url, messageHash, request, event)
            future.resolve(response)
        return await future

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']['private']
        client = self.client(url)
        event = 'login'
        future = client.future(event)
        authenticated = self.safe_value(client.subscriptions, event)
        if authenticated is None:
            nonce = self.milliseconds()
            payload = str(nonce) + ':' + self.apiKey
            signature = self.hmac(self.encode(payload), self.encode(self.secret))
            requestId = self.request_id()
            query = {
                'event': event,
                'data': {
                    'apiKey': self.apiKey,
                    'nonce': nonce,
                    'signature': signature,
                },
                'cid': requestId,
            }
            request = self.extend(query, params)
            messageHash = str(requestId)
            response = await self.watch(url, messageHash, request, event)
            #
            #     {
            #         data: {
            #             isAuthenticated: True,
            #             uid: '1362494'
            #         },
            #         rid: 2
            #     }
            #
            #     {
            #         data: {
            #             authError: {name: 'AuthLoginError', message: 'login failed'},
            #             isAuthenticated: False
            #         },
            #         rid: 2
            #     }
            #
            data = self.safe_value(response, 'data', {})
            isAuthenticated = self.safe_value(data, 'isAuthenticated', False)
            if isAuthenticated:
                future.resolve(response)
            else:
                raise AuthenticationError(self.id + ' ' + self.json(response))
        return await future

    async def watch_balance(self, params={}):
        await self.load_markets()
        await self.handshake(params)
        authentication = await self.authenticate(params)
        #
        #     {
        #         data: {
        #             isAuthenticated: True,
        #             uid: '1362494'
        #         },
        #         rid: 2
        #     }
        #
        data = self.safe_value(authentication, 'data', {})
        uid = self.safe_string(data, 'uid')
        url = self.urls['api']['ws']['private']
        defaultUserId = self.safe_string_2(self.options, 'userId', 'userID', uid)
        userId = self.safe_string_2(params, 'userId', 'userID', defaultUserId)
        defaultType = self.safe_string_2(self.options, 'watchBalance', 'defaultType', 'spot')
        type = self.safe_string(params, 'type', defaultType)
        query = self.omit(params, ['userId', 'userID', 'type'])
        channel = 'user/' + userId
        messageHash = type + ':balance'
        requestId = self.request_id()
        subscribe = {
            'event': '#subscribe',
            'data': {
                'channel': channel,
            },
            'cid': requestId,
        }
        request = self.deep_extend(subscribe, query)
        return await self.watch(url, messageHash, request, channel)

    def handle_balance(self, client, message):
        #
        #     {
        #         data: {
        #             unavailable: '40.00000000',
        #             available: '66.00400000',
        #             location: 'AAXGL',
        #             currency: 'USDT',
        #             purseType: 'SPTP',
        #             userID: '1362494'
        #         },
        #         event: 'USER_BALANCE'
        #     }
        #
        data = self.safe_value(message, 'data', {})
        purseType = self.safe_string(data, 'purseType')
        accounts = self.safe_value(self.options, 'accounts', {})
        accountType = self.safe_string(accounts, purseType)
        messageHash = accountType + ':balance'
        currencyId = self.safe_string(data, 'currency')
        code = self.safe_currency_code(currencyId)
        account = self.account()
        account['free'] = self.safe_string(data, 'available')
        account['used'] = self.safe_string(data, 'unavailable')
        if not (accountType in self.balance):
            self.balance[accountType] = {}
        self.balance[accountType][code] = account
        self.balance[accountType] = self.safe_balance(self.balance[accountType])
        client.resolve(self.balance[accountType], messageHash)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        await self.handshake(params)
        authentication = await self.authenticate(params)
        #
        #     {
        #         data: {
        #             isAuthenticated: True,
        #             uid: '1362494'
        #         },
        #         rid: 2
        #     }
        #
        data = self.safe_value(authentication, 'data', {})
        uid = self.safe_string(data, 'uid')
        url = self.urls['api']['ws']['private']
        defaultUserId = self.safe_string_2(self.options, 'userId', 'userID', uid)
        userId = self.safe_string_2(params, 'userId', 'userID', defaultUserId)
        query = self.omit(params, ['userId', 'userID'])
        channel = 'user/' + userId
        messageHash = 'orders'
        if symbol is not None:
            messageHash += ':' + symbol
        requestId = self.request_id()
        subscribe = {
            'event': '#subscribe',
            'data': {
                'channel': channel,
            },
            'cid': requestId,
        }
        request = self.deep_extend(subscribe, query)
        orders = await self.watch(url, messageHash, request, messageHash)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_order(self, client, message):
        #
        # spot
        #
        #     {
        #         data: {
        #             symbol: 'ETHUSDT',
        #             orderType: 2,
        #             avgPrice: '0',
        #             orderStatus: 5,
        #             userID: '1362494',
        #             quote: 'USDT',
        #             rejectCode: 0,
        #             price: '2000',
        #             orderQty: '0.02',
        #             commission: '0',
        #             id: '309458413831172096',
        #             timeInForce: 1,
        #             isTriggered: False,
        #             side: 1,
        #             orderID: '1qA7O2CnOo',
        #             leavesQty: '0',
        #             cumQty: '0',
        #             updateTime: '2021-05-03T14:37:26.498Z',
        #             lastQty: '0',
        #             stopPrice: '0',
        #             createTime: '2021-05-03T14:37:15.316Z',
        #             transactTime: '2021-05-03T14:37:26.492Z',
        #             base: 'ETH',
        #             lastPrice: '0'
        #         },
        #         event: 'SPOT'
        #     }
        #
        # futures
        #
        #     {
        #         data: {
        #             opens: {symbol: 'ETHUSDTFP', buy: 1, sell: 0},
        #             order: {
        #                 liqType: 0,
        #                 symbol: 'ETHUSDTFP',
        #                 orderType: 2,
        #                 leverage: '10',
        #                 marketPrice: '3283.4550000000',
        #                 code: 'FP',
        #                 avgPrice: '0',
        #                 orderStatus: 1,
        #                 userID: '1362494',
        #                 quote: 'USDT',
        #                 rejectCode: 0,
        #                 price: '2000',
        #                 orderQty: '1.0',
        #                 commission: '0',
        #                 id: '309633415658450944',
        #                 timeInForce: 1,
        #                 isTriggered: False,
        #                 side: 1,
        #                 orderID: '1qDemW8W1W',
        #                 leavesQty: '1.0',
        #                 cumQty: '0',
        #                 updateTime: '2021-05-04T02:12:39.024Z',
        #                 lastQty: '0',
        #                 stopPrice: '0',
        #                 createTime: '2021-05-04T02:12:39.007Z',
        #                 transactTime: '2021-05-04T02:12:39.018Z',
        #                 settleType: 'VANILLA',
        #                 base: 'ETH',
        #                 lastPrice: '0'
        #             }
        #         },
        #         event: 'FUTURES'
        #     }
        messageHash = 'orders'
        data = self.safe_value(message, 'data')
        order = self.safe_value(data, 'order')
        parsed = self.parse_order(data) if (order is None) else self.parse_order(order)
        symbol = self.safe_string(parsed, 'symbol')
        orderId = self.safe_string(parsed, 'id')
        if symbol is not None:
            if self.orders is None:
                limit = self.safe_integer(self.options, 'ordersLimit', 1000)
                self.orders = ArrayCacheBySymbolById(limit)
            cachedOrders = self.orders
            orders = self.safe_value(cachedOrders.hashmap, symbol, {})
            order = self.safe_value(orders, orderId)
            if order is not None:
                fee = self.safe_value(order, 'fee')
                if fee is not None:
                    parsed['fee'] = fee
                fees = self.safe_value(order, 'fees')
                if fees is not None:
                    parsed['fees'] = fees
                parsed['trades'] = self.safe_value(order, 'trades')
                parsed['timestamp'] = self.safe_integer(order, 'timestamp')
                parsed['datetime'] = self.safe_string(order, 'datetime')
            cachedOrders.append(parsed)
            client.resolve(self.orders, messageHash)
            messageHashSymbol = messageHash + ':' + symbol
            client.resolve(self.orders, messageHashSymbol)

    def handle_system_status(self, client, message):
        # {e: 'system', status: [{all: 'active'}]}
        return message

    def handle_subscription_status(self, client, message):
        #
        # public
        #
        #     {e: 'reply', status: 'ok'}
        #
        # private handshake response
        #
        #     {
        #         data: {
        #             id: 'SID-fqC6a7VTFG6X',
        #             info: "Invalid sid 'null', assigned a new one",
        #             isAuthenticated: False,
        #             pingTimeout: 68000
        #         },
        #         rid: 1
        #     }
        #
        rid = self.safe_string(message, 'rid')
        client.resolve(message, rid)
        return message

    async def pong(self, client, message):
        #
        #     "#1"
        #
        response = '#' + '2'
        await client.send(response)

    def handle_ping(self, client, message):
        self.spawn(self.pong, client, message)

    def handle_notification(self, client, message):
        #
        #     {
        #         "data": {
        #             "userID": "213409",
        #             "purseType": "coin",
        #             "currency": "BTC",
        #             "available": "0.12127194",
        #             "unavailable": "0.01458122"
        #         },
        #         "event": "USER_BALANCE"
        #     }
        #
        event = self.safe_value(message, 'event')
        methods = {
            'USER_FUNDS': self.handle_balance,
            'USER_BALANCE': self.handle_balance,
            'SPOT': self.handle_order,
            'FUTURES': self.handle_order,
        }
        method = self.safe_value(methods, event)
        if method is not None:
            return method(client, message)

    def handle_message(self, client, message):
        #
        #     {
        #         e: 'system',
        #         status: [
        #             {all: 'active'}
        #         ]
        #     }
        #
        #
        #     {
        #         asks: [
        #             ['54397.48000000', '0.002300'],
        #             ['54407.86000000', '1.880000'],
        #             ['54409.34000000', '0.046900'],
        #         ],
        #         bids: [
        #             ['54383.17000000', '1.380000'],
        #             ['54374.43000000', '1.880000'],
        #             ['54354.07000000', '0.013400'],
        #         ],
        #         e: 'BTCUSDT@book_20',
        #         t: 1619626148086
        #     }
        #
        # server may publish empty events if there is nothing to send right after a new connection is established
        #
        #     {"e":"empty"}
        #
        # private handshake response
        #
        #     {
        #         data: {
        #             id: 'SID-fqC6a7VTFG6X',
        #             info: "Invalid sid 'null', assigned a new one",
        #             isAuthenticated: False,
        #             pingTimeout: 68000
        #         },
        #         rid: 1
        #     }
        #
        # private balance update
        #
        #     {
        #         data: {
        #             channel: 'user/1362494',
        #             data: {
        #                 data: {
        #                     unavailable: '40.00000000',
        #                     available: '66.00400000',
        #                     location: 'AAXGL',
        #                     currency: 'USDT',
        #                     purseType: 'SPTP',
        #                     userID: '1362494'
        #                 },
        #                 event: 'USER_BALANCE'
        #             }
        #         },
        #         event: '#publish'
        #     }
        #
        # keepalive
        #
        #     #1
        #     #2
        #
        # private spot order update
        #
        #     {
        #         data: {
        #             channel: 'user/1362494',
        #             data: {
        #                 data: {
        #                     symbol: 'ETHUSDT',
        #                     orderType: 2,
        #                     avgPrice: '0',
        #                     orderStatus: 5,
        #                     userID: '1362494',
        #                     quote: 'USDT',
        #                     rejectCode: 0,
        #                     price: '2000',
        #                     orderQty: '0.02',
        #                     commission: '0',
        #                     id: '309458413831172096',
        #                     timeInForce: 1,
        #                     isTriggered: False,
        #                     side: 1,
        #                     orderID: '1qA7O2CnOo',
        #                     leavesQty: '0',
        #                     cumQty: '0',
        #                     updateTime: '2021-05-03T14:37:26.498Z',
        #                     lastQty: '0',
        #                     stopPrice: '0',
        #                     createTime: '2021-05-03T14:37:15.316Z',
        #                     transactTime: '2021-05-03T14:37:26.492Z',
        #                     base: 'ETH',
        #                     lastPrice: '0'
        #                 },
        #                 event: 'SPOT'
        #             }
        #         },
        #         event: '#publish'
        #     }
        #
        # private futures order update
        #
        #     {
        #         data: {
        #             channel: 'user/1362494',
        #             data: {
        #                 data: {
        #                     opens: {symbol: 'ETHUSDTFP', buy: 1, sell: 0},
        #                     order: {
        #                         liqType: 0,
        #                         symbol: 'ETHUSDTFP',
        #                         orderType: 2,
        #                         leverage: '10',
        #                         marketPrice: '3283.4550000000',
        #                         code: 'FP',
        #                         avgPrice: '0',
        #                         orderStatus: 1,
        #                         userID: '1362494',
        #                         quote: 'USDT',
        #                         rejectCode: 0,
        #                         price: '2000',
        #                         orderQty: '1.0',
        #                         commission: '0',
        #                         id: '309633415658450944',
        #                         timeInForce: 1,
        #                         isTriggered: False,
        #                         side: 1,
        #                         orderID: '1qDemW8W1W',
        #                         leavesQty: '1.0',
        #                         cumQty: '0',
        #                         updateTime: '2021-05-04T02:12:39.024Z',
        #                         lastQty: '0',
        #                         stopPrice: '0',
        #                         createTime: '2021-05-04T02:12:39.007Z',
        #                         transactTime: '2021-05-04T02:12:39.018Z',
        #                         settleType: 'VANILLA',
        #                         base: 'ETH',
        #                         lastPrice: '0'
        #                     }
        #                 },
        #                 event: 'FUTURES'
        #             }
        #         },
        #         event: '#publish'
        #     }
        #
        if isinstance(message, str):
            if message == '#1':
                self.handle_ping(client, message)
        else:
            event = self.safe_string(message, 'event')
            e = self.safe_string(message, 'e')
            if event == '#publish':
                # private
                contents = self.safe_value(message, 'data', {})
                data = self.safe_value(contents, 'data', {})
                self.handle_notification(client, data)
            elif e is None:
                # private
                rid = self.safe_string(message, 'rid')
                if rid is not None:
                    self.handle_subscription_status(client, message)
            else:
                # public
                parts = e.split('@')
                numParts = len(parts)
                methods = {
                    'reply': self.handle_subscription_status,
                    'system': self.handle_system_status,
                    'book': self.handle_order_book,
                    'trade': self.handle_trades,
                    'empty': None,  # server may publish empty events if there is nothing to send right after a new connection is established
                    'tickers': self.handle_tickers,
                    'candles': self.handle_ohlcv,
                    'done': self.handle_order,
                }
                method = None
                if numParts > 1:
                    nameLimit = self.safe_string(parts, 1)
                    subParts = nameLimit.split('_')
                    first = self.safe_string(subParts, 0)
                    second = self.safe_string(subParts, 1)
                    method = self.safe_value_2(methods, first, second)
                else:
                    name = self.safe_string(parts, 0)
                    method = self.safe_value(methods, name)
                if method is not None:
                    return method(client, message)
