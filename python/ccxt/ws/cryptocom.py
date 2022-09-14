# -*- coding: utf-8 -*-

# PLEASE DO NOT EDIT THIS FILE, IT IS GENERATED AND WILL BE OVERWRITTEN:
# https://github.com/ccxt/ccxt/blob/master/CONTRIBUTING.md#how-to-contribute-code

from ccxt.ws.base.exchange import Exchange
from ccxt.rest.async_support import cryptocom as cryptocomRest
from ccxt.ws.base.cache import ArrayCache, ArrayCacheBySymbolById, ArrayCacheByTimestamp
import hashlib
from ccxt.base.errors import ExchangeError
from ccxt.base.errors import AuthenticationError
from ccxt.base.errors import NotSupported


class cryptocom(Exchange, cryptocomRest):

    def describe(self):
        return self.deep_extend(super(cryptocom, self).describe(), {
            'has': {
                'ws': True,
                'watchBalance': True,
                'watchTicker': True,
                'watchTickers': False,  # for now
                'watchMyTrades': True,
                'watchTrades': True,
                'watchOrderBook': True,
                'watchOrders': True,
                'watchOHLCV': True,
            },
            'urls': {
                'api': {
                    'ws': {
                        'public': 'wss://stream.crypto.com/v2/market',
                        'private': 'wss://stream.crypto.com/v2/user',
                    },
                },
                'test': {
                    'public': 'wss://uat-stream.3ona.co/v2/market',
                    'private': 'wss://uat-stream.3ona.co/v2/user',
                },
            },
            'options': {
            },
            'streaming': {
            },
        })

    async def pong(self, client, message):
        # {
        #     "id": 1587523073344,
        #     "method": "public/heartbeat",
        #     "code": 0
        # }
        await client.send({'id': self.safe_integer(message, 'id'), 'method': 'public/respond-heartbeat'})

    async def watch_order_book(self, symbol, limit=None, params={}):
        if limit is not None:
            if (limit != 10) and (limit != 150):
                raise ExchangeError(self.id + ' watchOrderBook limit argument must be None, 10 or 150')
        else:
            limit = 150  # default value
        await self.load_markets()
        market = self.market(symbol)
        if not market['spot']:
            raise NotSupported(self.id + ' watchOrderBook() supports spot markets only')
        messageHash = 'book' + '.' + market['id'] + '.' + str(limit)
        orderbook = await self.watch_public(messageHash, params)
        return orderbook.limit(limit)

    def handle_order_book_snapshot(self, client, message):
        # full snapshot
        #
        # {
        #     "instrument_name":"LTC_USDT",
        #     "subscription":"book.LTC_USDT.150",
        #     "channel":"book",
        #     "depth":150,
        #     "data": [
        #          {
        #              'bids': [
        #                  [122.21, 0.74041, 4]
        #              ],
        #              'asks': [
        #                  [122.29, 0.00002, 1]
        #              ]
        #              't': 1648123943803,
        #              's':754560122
        #          }
        #      ]
        # }
        #
        messageHash = self.safe_string(message, 'subscription')
        marketId = self.safe_string(message, 'instrument_name')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        data = self.safe_value(message, 'data')
        data = self.safe_value(data, 0)
        timestamp = self.safe_integer(data, 't')
        snapshot = self.parse_order_book(data, symbol, timestamp)
        snapshot['nonce'] = self.safe_integer(data, 's')
        orderbook = self.safe_value(self.orderbooks, symbol)
        if orderbook is None:
            limit = self.safe_integer(message, 'depth')
            orderbook = self.order_book({}, limit)
        orderbook.reset(snapshot)
        self.orderbooks[symbol] = orderbook
        client.resolve(orderbook, messageHash)

    async def watch_trades(self, symbol, since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if not market['spot']:
            raise NotSupported(self.id + ' watchTrades() supports spot markets only')
        messageHash = 'trade' + '.' + market['id']
        trades = await self.watch_public(messageHash, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_since_limit(trades, since, limit, 'timestamp', True)

    def handle_trades(self, client, message):
        #
        # {
        #     code: 0,
        #     method: 'subscribe',
        #     result: {
        #       instrument_name: 'BTC_USDT',
        #       subscription: 'trade.BTC_USDT',
        #       channel: 'trade',
        #       data: [
        #             {
        #                 "dataTime":1648122434405,
        #                 "d":"2358394540212355488",
        #                 "s":"SELL",
        #                 "p":42980.85,
        #                 "q":0.002325,
        #                 "t":1648122434404,
        #                 "i":"BTC_USDT"
        #              }
        #              (...)
        #       ]
        # }
        #
        channel = self.safe_string(message, 'channel')
        marketId = self.safe_string(message, 'instrument_name')
        symbolSpecificMessageHash = self.safe_string(message, 'subscription')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        stored = self.safe_value(self.trades, symbol)
        if stored is None:
            limit = self.safe_integer(self.options, 'tradesLimit', 1000)
            stored = ArrayCache(limit)
            self.trades[symbol] = stored
        data = self.safe_value(message, 'data', [])
        parsedTrades = self.parse_trades(data, market)
        for j in range(0, len(parsedTrades)):
            stored.append(parsedTrades[j])
        client.resolve(stored, symbolSpecificMessageHash)
        client.resolve(stored, channel)

    async def watch_my_trades(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        defaultType = self.safe_string(self.options, 'defaultType', 'spot')
        messageHash = 'user.margin.trade' if (defaultType == 'margin') else 'user.trade'
        messageHash = (messageHash + '.' + market['id']) if (market is not None) else messageHash
        trades = await self.watch_private(messageHash, params)
        if self.newUpdates:
            limit = trades.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(trades, symbol, since, limit, True)

    async def watch_ticker(self, symbol, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if not market['spot']:
            raise NotSupported(self.id + ' watchTicker() supports spot markets only')
        messageHash = 'ticker' + '.' + market['id']
        return await self.watch_public(messageHash, params)

    def handle_ticker(self, client, message):
        #
        # {
        #     "info":{
        #        "instrument_name":"BTC_USDT",
        #        "subscription":"ticker.BTC_USDT",
        #        "channel":"ticker",
        #        "data":[
        #           {
        #              "i":"BTC_USDT",
        #              "b":43063.19,
        #              "k":43063.2,
        #              "a":43063.19,
        #              "t":1648121165658,
        #              "v":43573.912409,
        #              "h":43498.51,
        #              "l":41876.58,
        #              "c":1087.43
        #           }
        #        ]
        #     }
        #  }
        #
        messageHash = self.safe_string(message, 'subscription')
        marketId = self.safe_string(message, 'instrument_name')
        market = self.safe_market(marketId)
        data = self.safe_value(message, 'data', [])
        for i in range(0, len(data)):
            ticker = data[i]
            parsed = self.parse_ticker(ticker, market)
            symbol = parsed['symbol']
            self.tickers[symbol] = parsed
            client.resolve(parsed, messageHash)

    async def watch_ohlcv(self, symbol, timeframe='1m', since=None, limit=None, params={}):
        await self.load_markets()
        market = self.market(symbol)
        if not market['spot']:
            raise NotSupported(self.id + ' watchOHLCV() supports spot markets only')
        interval = self.timeframes[timeframe]
        messageHash = 'candlestick' + '.' + interval + '.' + market['id']
        ohlcv = await self.watch_public(messageHash, params)
        if self.newUpdates:
            limit = ohlcv.getLimit(symbol, limit)
        return self.filter_by_since_limit(ohlcv, since, limit, 0, True)

    def handle_ohlcv(self, client, message):
        #
        #  {
        #       instrument_name: 'BTC_USDT',
        #       subscription: 'candlestick.1m.BTC_USDT',
        #       channel: 'candlestick',
        #       depth: 300,
        #       interval: '1m',
        #       data: [[Object]]
        #   }
        #
        messageHash = self.safe_string(message, 'subscription')
        marketId = self.safe_string(message, 'instrument_name')
        market = self.safe_market(marketId)
        symbol = market['symbol']
        interval = self.safe_string(message, 'interval')
        timeframe = self.find_timeframe(interval)
        self.ohlcvs[symbol] = self.safe_value(self.ohlcvs, symbol, {})
        stored = self.safe_value(self.ohlcvs[symbol], timeframe)
        if stored is None:
            limit = self.safe_integer(self.options, 'OHLCVLimit', 1000)
            stored = ArrayCacheByTimestamp(limit)
            self.ohlcvs[symbol][timeframe] = stored
        data = self.safe_value(message, 'data')
        for i in range(0, len(data)):
            tick = data[i]
            parsed = self.parse_ohlcv(tick, market)
            stored.append(parsed)
        client.resolve(stored, messageHash)

    async def watch_orders(self, symbol=None, since=None, limit=None, params={}):
        await self.load_markets()
        market = None
        if symbol is not None:
            market = self.market(symbol)
        defaultType = self.safe_string(self.options, 'defaultType', 'spot')
        messageHash = 'user.margin.order' if (defaultType == 'margin') else 'user.order'
        messageHash = (messageHash + '.' + market['id']) if (market is not None) else messageHash
        orders = await self.watch_private(messageHash, params)
        if self.newUpdates:
            limit = orders.getLimit(symbol, limit)
        return self.filter_by_symbol_since_limit(orders, symbol, since, limit, True)

    def handle_orders(self, client, message, subscription=None):
        #
        # {
        #     "method": "subscribe",
        #     "result": {
        #       "instrument_name": "ETH_CRO",
        #       "subscription": "user.order.ETH_CRO",
        #       "channel": "user.order",
        #       "data": [
        #         {
        #           "status": "ACTIVE",
        #           "side": "BUY",
        #           "price": 1,
        #           "quantity": 1,
        #           "order_id": "366455245775097673",
        #           "client_oid": "my_order_0002",
        #           "create_time": 1588758017375,
        #           "update_time": 1588758017411,
        #           "type": "LIMIT",
        #           "instrument_name": "ETH_CRO",
        #           "cumulative_quantity": 0,
        #           "cumulative_value": 0,
        #           "avg_price": 0,
        #           "fee_currency": "CRO",
        #           "time_in_force":"GOOD_TILL_CANCEL"
        #         }
        #       ],
        #       "channel": "user.order.ETH_CRO"
        #     }
        #
        channel = self.safe_string(message, 'channel')
        symbolSpecificMessageHash = self.safe_string(message, 'subscription')
        orders = self.safe_value(message, 'data', [])
        ordersLength = len(orders)
        if ordersLength > 0:
            if self.orders is None:
                limit = self.safe_integer(self.options, 'ordersLimit', 1000)
                self.orders = ArrayCacheBySymbolById(limit)
            stored = self.orders
            parsed = self.parse_orders(orders)
            for i in range(0, len(parsed)):
                stored.append(parsed[i])
            client.resolve(stored, symbolSpecificMessageHash)
            # non-symbol specific
            client.resolve(stored, channel)

    async def watch_balance(self, params={}):
        defaultType = self.safe_string(self.options, 'defaultType', 'spot')
        messageHash = 'user.margin.balance' if (defaultType == 'margin') else 'user.balance'
        return await self.watch_private(messageHash, params)

    def handle_balance(self, client, message):
        #
        # {
        #     "method": "subscribe",
        #     "result": {
        #       "subscription": "user.balance",
        #       "channel": "user.balance",
        #       "data": [
        #         {
        #           "currency": "CRO",
        #           "balance": 99999999947.99626,
        #           "available": 99999988201.50826,
        #           "order": 11746.488,
        #           "stake": 0
        #         }
        #       ],
        #       "channel": "user.balance"
        #     }
        # }
        #
        messageHash = self.safe_string(message, 'subscription')
        data = self.safe_value(message, 'data')
        for i in range(0, len(data)):
            balance = data[i]
            currencyId = self.safe_string(balance, 'currency')
            code = self.safe_currency_code(currencyId)
            account = self.account()
            account['free'] = self.safe_string(balance, 'available')
            account['total'] = self.safe_string(balance, 'balance')
            self.balance[code] = account
            self.balance = self.safe_balance(self.balance)
        client.resolve(self.balance, messageHash)

    async def watch_public(self, messageHash, params={}):
        url = self.urls['api']['ws']['public']
        id = self.nonce()
        request = {
            'method': 'subscribe',
            'params': {
                'channels': [messageHash],
            },
            'nonce': id,
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    async def watch_private(self, messageHash, params={}):
        await self.authenticate()
        url = self.urls['api']['ws']['private']
        id = self.nonce()
        request = {
            'method': 'subscribe',
            'params': {
                'channels': [messageHash],
            },
            'nonce': id,
        }
        message = self.extend(request, params)
        return await self.watch(url, messageHash, message, messageHash)

    def handle_error_message(self, client, message):
        # {
        #     id: 0,
        #     code: 10004,
        #     method: 'subscribe',
        #     message: 'invalid channel {"channels":["trade.BTCUSD-PERP"]}'
        # }
        errorCode = self.safe_integer(message, 'code')
        try:
            if errorCode is not None and errorCode != 0:
                feedback = self.id + ' ' + self.json(message)
                self.throw_exactly_matched_exception(self.exceptions['exact'], errorCode, feedback)
                messageString = self.safe_value(message, 'message')
                if messageString is not None:
                    self.throw_broadly_matched_exception(self.exceptions['broad'], messageString, feedback)
        except Exception as e:
            if isinstance(e, AuthenticationError):
                client.reject(e, 'authenticated')
                if 'public/auth' in client.subscriptions:
                    del client.subscriptions['public/auth']
                return False
            else:
                client.reject(e)
        return message

    def handle_message(self, client, message):
        # ping
        # {
        #     "id": 1587523073344,
        #     "method": "public/heartbeat",
        #     "code": 0
        # }
        # auth
        #  {id: 1648132625434, method: 'public/auth', code: 0}
        # ohlcv
        # {
        #     code: 0,
        #     method: 'subscribe',
        #     result: {
        #       instrument_name: 'BTC_USDT',
        #       subscription: 'candlestick.1m.BTC_USDT',
        #       channel: 'candlestick',
        #       depth: 300,
        #       interval: '1m',
        #       data: [[Object]]
        #     }
        #   }
        # ticker
        # {
        #     "info":{
        #        "instrument_name":"BTC_USDT",
        #        "subscription":"ticker.BTC_USDT",
        #        "channel":"ticker",
        #        "data":[{}]
        #
        if not self.handle_error_message(client, message):
            return
        subject = self.safe_string(message, 'method')
        if subject == 'public/heartbeat':
            self.handle_ping(client, message)
            return
        if subject == 'public/auth':
            self.handle_authenticate(client, message)
            return
        methods = {
            'candlestick': self.handle_ohlcv,
            'ticker': self.handle_ticker,
            'trade': self.handle_trades,
            'book': self.handle_order_book_snapshot,
            'user.order': self.handle_orders,
            'user.margin.order': self.handle_orders,
            'user.trade': self.handle_trades,
            'user.margin.trade': self.handle_trades,
            'user.balance': self.handle_balance,
            'user.margin.balance': self.handle_balance,
        }
        result = self.safe_value_2(message, 'result', 'info')
        channel = self.safe_string(result, 'channel')
        method = self.safe_value(methods, channel)
        if method is not None:
            method(client, result)

    async def authenticate(self, params={}):
        url = self.urls['api']['ws']['private']
        self.check_required_credentials()
        client = self.client(url)
        future = client.future('authenticated')
        messageHash = 'public/auth'
        authenticated = self.safe_value(client.subscriptions, messageHash)
        if authenticated is None:
            nonce = str(self.nonce())
            auth = messageHash + nonce + self.apiKey + nonce
            signature = self.hmac(self.encode(auth), self.encode(self.secret), hashlib.sha256)
            request = {
                'id': nonce,
                'nonce': nonce,
                'method': messageHash,
                'api_key': self.apiKey,
                'sig': signature,
            }
            self.spawn(self.watch, url, messageHash, self.extend(request, params), messageHash)
        return await future

    def handle_ping(self, client, message):
        self.spawn(self.pong, client, message)

    def handle_authenticate(self, client, message):
        #
        #  {id: 1648132625434, method: 'public/auth', code: 0}
        #
        future = client.futures['authenticated']
        future.resolve(1)
        client.resolve(1, 'public/auth')
        return message
