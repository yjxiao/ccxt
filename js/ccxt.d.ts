import { Exchange } from './src/base/Exchange.js';
import { Precise } from './src/base/Precise.js';
import * as functions from './src/base/functions.js';
import * as errors from './src/base/errors.js';
import type { Market, Trade, Fee, Ticker, OrderBook, Order, Transaction, Tickers, Currency, Balance, DepositAddress, WithdrawalResponse, DepositAddressResponse, OHLCV, Balances, PartialBalances, Dictionary, MinMax, Position, FundingRateHistory, Liquidation, FundingHistory, MarginMode, Greeks, Leverage, Leverages, Option, OptionChain } from './src/base/types.js';
import { BaseError, ExchangeError, PermissionDenied, AccountNotEnabled, AccountSuspended, ArgumentsRequired, BadRequest, BadSymbol, MarginModeAlreadySet, BadResponse, NullResponse, InsufficientFunds, InvalidAddress, InvalidOrder, OrderNotFound, OrderNotCached, CancelPending, OrderImmediatelyFillable, OrderNotFillable, DuplicateOrderId, NotSupported, NetworkError, DDoSProtection, RateLimitExceeded, ExchangeNotAvailable, OnMaintenance, InvalidNonce, RequestTimeout, AuthenticationError, AddressPending, NoChange } from './src/base/errors.js';
declare const version = "4.2.86";
import ace from './src/ace.js';
import alpaca from './src/alpaca.js';
import ascendex from './src/ascendex.js';
import bequant from './src/bequant.js';
import bigone from './src/bigone.js';
import binance from './src/binance.js';
import binancecoinm from './src/binancecoinm.js';
import binanceus from './src/binanceus.js';
import binanceusdm from './src/binanceusdm.js';
import bingx from './src/bingx.js';
import bit2c from './src/bit2c.js';
import bitbank from './src/bitbank.js';
import bitbay from './src/bitbay.js';
import bitbns from './src/bitbns.js';
import bitcoincom from './src/bitcoincom.js';
import bitfinex from './src/bitfinex.js';
import bitfinex2 from './src/bitfinex2.js';
import bitflyer from './src/bitflyer.js';
import bitget from './src/bitget.js';
import bithumb from './src/bithumb.js';
import bitmart from './src/bitmart.js';
import bitmex from './src/bitmex.js';
import bitopro from './src/bitopro.js';
import bitpanda from './src/bitpanda.js';
import bitrue from './src/bitrue.js';
import bitso from './src/bitso.js';
import bitstamp from './src/bitstamp.js';
import bitteam from './src/bitteam.js';
import bitvavo from './src/bitvavo.js';
import bl3p from './src/bl3p.js';
import blockchaincom from './src/blockchaincom.js';
import blofin from './src/blofin.js';
import btcalpha from './src/btcalpha.js';
import btcbox from './src/btcbox.js';
import btcmarkets from './src/btcmarkets.js';
import btcturk from './src/btcturk.js';
import bybit from './src/bybit.js';
import cex from './src/cex.js';
import coinbase from './src/coinbase.js';
import coinbaseinternational from './src/coinbaseinternational.js';
import coinbasepro from './src/coinbasepro.js';
import coincheck from './src/coincheck.js';
import coinex from './src/coinex.js';
import coinlist from './src/coinlist.js';
import coinmate from './src/coinmate.js';
import coinmetro from './src/coinmetro.js';
import coinone from './src/coinone.js';
import coinsph from './src/coinsph.js';
import coinspot from './src/coinspot.js';
import cryptocom from './src/cryptocom.js';
import currencycom from './src/currencycom.js';
import delta from './src/delta.js';
import deribit from './src/deribit.js';
import digifinex from './src/digifinex.js';
import exmo from './src/exmo.js';
import fmfwio from './src/fmfwio.js';
import gate from './src/gate.js';
import gateio from './src/gateio.js';
import gemini from './src/gemini.js';
import hitbtc from './src/hitbtc.js';
import hitbtc3 from './src/hitbtc3.js';
import hollaex from './src/hollaex.js';
import htx from './src/htx.js';
import huobi from './src/huobi.js';
import huobijp from './src/huobijp.js';
import hyperliquid from './src/hyperliquid.js';
import idex from './src/idex.js';
import independentreserve from './src/independentreserve.js';
import indodax from './src/indodax.js';
import kraken from './src/kraken.js';
import krakenfutures from './src/krakenfutures.js';
import kucoin from './src/kucoin.js';
import kucoinfutures from './src/kucoinfutures.js';
import kuna from './src/kuna.js';
import latoken from './src/latoken.js';
import lbank from './src/lbank.js';
import luno from './src/luno.js';
import lykke from './src/lykke.js';
import mercado from './src/mercado.js';
import mexc from './src/mexc.js';
import ndax from './src/ndax.js';
import novadax from './src/novadax.js';
import oceanex from './src/oceanex.js';
import okcoin from './src/okcoin.js';
import okx from './src/okx.js';
import onetrading from './src/onetrading.js';
import p2b from './src/p2b.js';
import paymium from './src/paymium.js';
import phemex from './src/phemex.js';
import poloniex from './src/poloniex.js';
import poloniexfutures from './src/poloniexfutures.js';
import probit from './src/probit.js';
import timex from './src/timex.js';
import tokocrypto from './src/tokocrypto.js';
import tradeogre from './src/tradeogre.js';
import upbit from './src/upbit.js';
import wavesexchange from './src/wavesexchange.js';
import wazirx from './src/wazirx.js';
import whitebit from './src/whitebit.js';
import woo from './src/woo.js';
import yobit from './src/yobit.js';
import zaif from './src/zaif.js';
import zonda from './src/zonda.js';
import alpacaPro from './src/pro/alpaca.js';
import ascendexPro from './src/pro/ascendex.js';
import bequantPro from './src/pro/bequant.js';
import binancePro from './src/pro/binance.js';
import binancecoinmPro from './src/pro/binancecoinm.js';
import binanceusPro from './src/pro/binanceus.js';
import binanceusdmPro from './src/pro/binanceusdm.js';
import bingxPro from './src/pro/bingx.js';
import bitcoincomPro from './src/pro/bitcoincom.js';
import bitfinexPro from './src/pro/bitfinex.js';
import bitfinex2Pro from './src/pro/bitfinex2.js';
import bitgetPro from './src/pro/bitget.js';
import bithumbPro from './src/pro/bithumb.js';
import bitmartPro from './src/pro/bitmart.js';
import bitmexPro from './src/pro/bitmex.js';
import bitoproPro from './src/pro/bitopro.js';
import bitpandaPro from './src/pro/bitpanda.js';
import bitruePro from './src/pro/bitrue.js';
import bitstampPro from './src/pro/bitstamp.js';
import bitvavoPro from './src/pro/bitvavo.js';
import blockchaincomPro from './src/pro/blockchaincom.js';
import bybitPro from './src/pro/bybit.js';
import cexPro from './src/pro/cex.js';
import coinbasePro from './src/pro/coinbase.js';
import coinbaseinternationalPro from './src/pro/coinbaseinternational.js';
import coinbaseproPro from './src/pro/coinbasepro.js';
import coincheckPro from './src/pro/coincheck.js';
import coinexPro from './src/pro/coinex.js';
import coinonePro from './src/pro/coinone.js';
import cryptocomPro from './src/pro/cryptocom.js';
import currencycomPro from './src/pro/currencycom.js';
import deribitPro from './src/pro/deribit.js';
import exmoPro from './src/pro/exmo.js';
import gatePro from './src/pro/gate.js';
import gateioPro from './src/pro/gateio.js';
import geminiPro from './src/pro/gemini.js';
import hitbtcPro from './src/pro/hitbtc.js';
import hollaexPro from './src/pro/hollaex.js';
import htxPro from './src/pro/htx.js';
import huobiPro from './src/pro/huobi.js';
import huobijpPro from './src/pro/huobijp.js';
import hyperliquidPro from './src/pro/hyperliquid.js';
import idexPro from './src/pro/idex.js';
import independentreservePro from './src/pro/independentreserve.js';
import krakenPro from './src/pro/kraken.js';
import krakenfuturesPro from './src/pro/krakenfutures.js';
import kucoinPro from './src/pro/kucoin.js';
import kucoinfuturesPro from './src/pro/kucoinfutures.js';
import lbankPro from './src/pro/lbank.js';
import lunoPro from './src/pro/luno.js';
import mexcPro from './src/pro/mexc.js';
import ndaxPro from './src/pro/ndax.js';
import okcoinPro from './src/pro/okcoin.js';
import okxPro from './src/pro/okx.js';
import onetradingPro from './src/pro/onetrading.js';
import p2bPro from './src/pro/p2b.js';
import phemexPro from './src/pro/phemex.js';
import poloniexPro from './src/pro/poloniex.js';
import poloniexfuturesPro from './src/pro/poloniexfutures.js';
import probitPro from './src/pro/probit.js';
import upbitPro from './src/pro/upbit.js';
import wazirxPro from './src/pro/wazirx.js';
import whitebitPro from './src/pro/whitebit.js';
import wooPro from './src/pro/woo.js';
declare const exchanges: {
    ace: typeof ace;
    alpaca: typeof alpaca;
    ascendex: typeof ascendex;
    bequant: typeof bequant;
    bigone: typeof bigone;
    binance: typeof binance;
    binancecoinm: typeof binancecoinm;
    binanceus: typeof binanceus;
    binanceusdm: typeof binanceusdm;
    bingx: typeof bingx;
    bit2c: typeof bit2c;
    bitbank: typeof bitbank;
    bitbay: typeof bitbay;
    bitbns: typeof bitbns;
    bitcoincom: typeof bitcoincom;
    bitfinex: typeof bitfinex;
    bitfinex2: typeof bitfinex2;
    bitflyer: typeof bitflyer;
    bitget: typeof bitget;
    bithumb: typeof bithumb;
    bitmart: typeof bitmart;
    bitmex: typeof bitmex;
    bitopro: typeof bitopro;
    bitpanda: typeof bitpanda;
    bitrue: typeof bitrue;
    bitso: typeof bitso;
    bitstamp: typeof bitstamp;
    bitteam: typeof bitteam;
    bitvavo: typeof bitvavo;
    bl3p: typeof bl3p;
    blockchaincom: typeof blockchaincom;
    blofin: typeof blofin;
    btcalpha: typeof btcalpha;
    btcbox: typeof btcbox;
    btcmarkets: typeof btcmarkets;
    btcturk: typeof btcturk;
    bybit: typeof bybit;
    cex: typeof cex;
    coinbase: typeof coinbase;
    coinbaseinternational: typeof coinbaseinternational;
    coinbasepro: typeof coinbasepro;
    coincheck: typeof coincheck;
    coinex: typeof coinex;
    coinlist: typeof coinlist;
    coinmate: typeof coinmate;
    coinmetro: typeof coinmetro;
    coinone: typeof coinone;
    coinsph: typeof coinsph;
    coinspot: typeof coinspot;
    cryptocom: typeof cryptocom;
    currencycom: typeof currencycom;
    delta: typeof delta;
    deribit: typeof deribit;
    digifinex: typeof digifinex;
    exmo: typeof exmo;
    fmfwio: typeof fmfwio;
    gate: typeof gate;
    gateio: typeof gateio;
    gemini: typeof gemini;
    hitbtc: typeof hitbtc;
    hitbtc3: typeof hitbtc3;
    hollaex: typeof hollaex;
    htx: typeof htx;
    huobi: typeof huobi;
    huobijp: typeof huobijp;
    hyperliquid: typeof hyperliquid;
    idex: typeof idex;
    independentreserve: typeof independentreserve;
    indodax: typeof indodax;
    kraken: typeof kraken;
    krakenfutures: typeof krakenfutures;
    kucoin: typeof kucoin;
    kucoinfutures: typeof kucoinfutures;
    kuna: typeof kuna;
    latoken: typeof latoken;
    lbank: typeof lbank;
    luno: typeof luno;
    lykke: typeof lykke;
    mercado: typeof mercado;
    mexc: typeof mexc;
    ndax: typeof ndax;
    novadax: typeof novadax;
    oceanex: typeof oceanex;
    okcoin: typeof okcoin;
    okx: typeof okx;
    onetrading: typeof onetrading;
    p2b: typeof p2b;
    paymium: typeof paymium;
    phemex: typeof phemex;
    poloniex: typeof poloniex;
    poloniexfutures: typeof poloniexfutures;
    probit: typeof probit;
    timex: typeof timex;
    tokocrypto: typeof tokocrypto;
    tradeogre: typeof tradeogre;
    upbit: typeof upbit;
    wavesexchange: typeof wavesexchange;
    wazirx: typeof wazirx;
    whitebit: typeof whitebit;
    woo: typeof woo;
    yobit: typeof yobit;
    zaif: typeof zaif;
    zonda: typeof zonda;
};
declare const pro: {
    alpaca: typeof alpacaPro;
    ascendex: typeof ascendexPro;
    bequant: typeof bequantPro;
    binance: typeof binancePro;
    binancecoinm: typeof binancecoinmPro;
    binanceus: typeof binanceusPro;
    binanceusdm: typeof binanceusdmPro;
    bingx: typeof bingxPro;
    bitcoincom: typeof bitcoincomPro;
    bitfinex: typeof bitfinexPro;
    bitfinex2: typeof bitfinex2Pro;
    bitget: typeof bitgetPro;
    bithumb: typeof bithumbPro;
    bitmart: typeof bitmartPro;
    bitmex: typeof bitmexPro;
    bitopro: typeof bitoproPro;
    bitpanda: typeof bitpandaPro;
    bitrue: typeof bitruePro;
    bitstamp: typeof bitstampPro;
    bitvavo: typeof bitvavoPro;
    blockchaincom: typeof blockchaincomPro;
    bybit: typeof bybitPro;
    cex: typeof cexPro;
    coinbase: typeof coinbasePro;
    coinbaseinternational: typeof coinbaseinternationalPro;
    coinbasepro: typeof coinbaseproPro;
    coincheck: typeof coincheckPro;
    coinex: typeof coinexPro;
    coinone: typeof coinonePro;
    cryptocom: typeof cryptocomPro;
    currencycom: typeof currencycomPro;
    deribit: typeof deribitPro;
    exmo: typeof exmoPro;
    gate: typeof gatePro;
    gateio: typeof gateioPro;
    gemini: typeof geminiPro;
    hitbtc: typeof hitbtcPro;
    hollaex: typeof hollaexPro;
    htx: typeof htxPro;
    huobi: typeof huobiPro;
    huobijp: typeof huobijpPro;
    hyperliquid: typeof hyperliquidPro;
    idex: typeof idexPro;
    independentreserve: typeof independentreservePro;
    kraken: typeof krakenPro;
    krakenfutures: typeof krakenfuturesPro;
    kucoin: typeof kucoinPro;
    kucoinfutures: typeof kucoinfuturesPro;
    lbank: typeof lbankPro;
    luno: typeof lunoPro;
    mexc: typeof mexcPro;
    ndax: typeof ndaxPro;
    okcoin: typeof okcoinPro;
    okx: typeof okxPro;
    onetrading: typeof onetradingPro;
    p2b: typeof p2bPro;
    phemex: typeof phemexPro;
    poloniex: typeof poloniexPro;
    poloniexfutures: typeof poloniexfuturesPro;
    probit: typeof probitPro;
    upbit: typeof upbitPro;
    wazirx: typeof wazirxPro;
    whitebit: typeof whitebitPro;
    woo: typeof wooPro;
};
declare const ccxt: {
    version: string;
    Exchange: typeof Exchange;
    Precise: typeof Precise;
    exchanges: string[];
    pro: {
        alpaca: typeof alpacaPro;
        ascendex: typeof ascendexPro;
        bequant: typeof bequantPro;
        binance: typeof binancePro;
        binancecoinm: typeof binancecoinmPro;
        binanceus: typeof binanceusPro;
        binanceusdm: typeof binanceusdmPro;
        bingx: typeof bingxPro;
        bitcoincom: typeof bitcoincomPro;
        bitfinex: typeof bitfinexPro;
        bitfinex2: typeof bitfinex2Pro;
        bitget: typeof bitgetPro;
        bithumb: typeof bithumbPro;
        bitmart: typeof bitmartPro;
        bitmex: typeof bitmexPro;
        bitopro: typeof bitoproPro;
        bitpanda: typeof bitpandaPro;
        bitrue: typeof bitruePro;
        bitstamp: typeof bitstampPro;
        bitvavo: typeof bitvavoPro;
        blockchaincom: typeof blockchaincomPro;
        bybit: typeof bybitPro;
        cex: typeof cexPro;
        coinbase: typeof coinbasePro;
        coinbaseinternational: typeof coinbaseinternationalPro;
        coinbasepro: typeof coinbaseproPro;
        coincheck: typeof coincheckPro;
        coinex: typeof coinexPro;
        coinone: typeof coinonePro;
        cryptocom: typeof cryptocomPro;
        currencycom: typeof currencycomPro;
        deribit: typeof deribitPro;
        exmo: typeof exmoPro;
        gate: typeof gatePro;
        gateio: typeof gateioPro;
        gemini: typeof geminiPro;
        hitbtc: typeof hitbtcPro;
        hollaex: typeof hollaexPro;
        htx: typeof htxPro;
        huobi: typeof huobiPro;
        huobijp: typeof huobijpPro;
        hyperliquid: typeof hyperliquidPro;
        idex: typeof idexPro;
        independentreserve: typeof independentreservePro;
        kraken: typeof krakenPro;
        krakenfutures: typeof krakenfuturesPro;
        kucoin: typeof kucoinPro;
        kucoinfutures: typeof kucoinfuturesPro;
        lbank: typeof lbankPro;
        luno: typeof lunoPro;
        mexc: typeof mexcPro;
        ndax: typeof ndaxPro;
        okcoin: typeof okcoinPro;
        okx: typeof okxPro;
        onetrading: typeof onetradingPro;
        p2b: typeof p2bPro;
        phemex: typeof phemexPro;
        poloniex: typeof poloniexPro;
        poloniexfutures: typeof poloniexfuturesPro;
        probit: typeof probitPro;
        upbit: typeof upbitPro;
        wazirx: typeof wazirxPro;
        whitebit: typeof whitebitPro;
        woo: typeof wooPro;
    };
} & {
    ace: typeof ace;
    alpaca: typeof alpaca;
    ascendex: typeof ascendex;
    bequant: typeof bequant;
    bigone: typeof bigone;
    binance: typeof binance;
    binancecoinm: typeof binancecoinm;
    binanceus: typeof binanceus;
    binanceusdm: typeof binanceusdm;
    bingx: typeof bingx;
    bit2c: typeof bit2c;
    bitbank: typeof bitbank;
    bitbay: typeof bitbay;
    bitbns: typeof bitbns;
    bitcoincom: typeof bitcoincom;
    bitfinex: typeof bitfinex;
    bitfinex2: typeof bitfinex2;
    bitflyer: typeof bitflyer;
    bitget: typeof bitget;
    bithumb: typeof bithumb;
    bitmart: typeof bitmart;
    bitmex: typeof bitmex;
    bitopro: typeof bitopro;
    bitpanda: typeof bitpanda;
    bitrue: typeof bitrue;
    bitso: typeof bitso;
    bitstamp: typeof bitstamp;
    bitteam: typeof bitteam;
    bitvavo: typeof bitvavo;
    bl3p: typeof bl3p;
    blockchaincom: typeof blockchaincom;
    blofin: typeof blofin;
    btcalpha: typeof btcalpha;
    btcbox: typeof btcbox;
    btcmarkets: typeof btcmarkets;
    btcturk: typeof btcturk;
    bybit: typeof bybit;
    cex: typeof cex;
    coinbase: typeof coinbase;
    coinbaseinternational: typeof coinbaseinternational;
    coinbasepro: typeof coinbasepro;
    coincheck: typeof coincheck;
    coinex: typeof coinex;
    coinlist: typeof coinlist;
    coinmate: typeof coinmate;
    coinmetro: typeof coinmetro;
    coinone: typeof coinone;
    coinsph: typeof coinsph;
    coinspot: typeof coinspot;
    cryptocom: typeof cryptocom;
    currencycom: typeof currencycom;
    delta: typeof delta;
    deribit: typeof deribit;
    digifinex: typeof digifinex;
    exmo: typeof exmo;
    fmfwio: typeof fmfwio;
    gate: typeof gate;
    gateio: typeof gateio;
    gemini: typeof gemini;
    hitbtc: typeof hitbtc;
    hitbtc3: typeof hitbtc3;
    hollaex: typeof hollaex;
    htx: typeof htx;
    huobi: typeof huobi;
    huobijp: typeof huobijp;
    hyperliquid: typeof hyperliquid;
    idex: typeof idex;
    independentreserve: typeof independentreserve;
    indodax: typeof indodax;
    kraken: typeof kraken;
    krakenfutures: typeof krakenfutures;
    kucoin: typeof kucoin;
    kucoinfutures: typeof kucoinfutures;
    kuna: typeof kuna;
    latoken: typeof latoken;
    lbank: typeof lbank;
    luno: typeof luno;
    lykke: typeof lykke;
    mercado: typeof mercado;
    mexc: typeof mexc;
    ndax: typeof ndax;
    novadax: typeof novadax;
    oceanex: typeof oceanex;
    okcoin: typeof okcoin;
    okx: typeof okx;
    onetrading: typeof onetrading;
    p2b: typeof p2b;
    paymium: typeof paymium;
    phemex: typeof phemex;
    poloniex: typeof poloniex;
    poloniexfutures: typeof poloniexfutures;
    probit: typeof probit;
    timex: typeof timex;
    tokocrypto: typeof tokocrypto;
    tradeogre: typeof tradeogre;
    upbit: typeof upbit;
    wavesexchange: typeof wavesexchange;
    wazirx: typeof wazirx;
    whitebit: typeof whitebit;
    woo: typeof woo;
    yobit: typeof yobit;
    zaif: typeof zaif;
    zonda: typeof zonda;
} & typeof functions & typeof errors;
export { version, Exchange, exchanges, pro, Precise, functions, errors, BaseError, ExchangeError, PermissionDenied, AccountNotEnabled, AccountSuspended, ArgumentsRequired, BadRequest, BadSymbol, MarginModeAlreadySet, BadResponse, NullResponse, InsufficientFunds, InvalidAddress, InvalidOrder, OrderNotFound, OrderNotCached, CancelPending, OrderImmediatelyFillable, OrderNotFillable, DuplicateOrderId, NotSupported, NetworkError, DDoSProtection, RateLimitExceeded, ExchangeNotAvailable, OnMaintenance, InvalidNonce, RequestTimeout, AuthenticationError, AddressPending, NoChange, Market, Trade, Fee, Ticker, OrderBook, Order, Transaction, Tickers, Currency, Balance, DepositAddress, WithdrawalResponse, DepositAddressResponse, OHLCV, Balances, PartialBalances, Dictionary, MinMax, Position, FundingRateHistory, Liquidation, FundingHistory, MarginMode, Greeks, Leverage, Leverages, Option, OptionChain, ace, alpaca, ascendex, bequant, bigone, binance, binancecoinm, binanceus, binanceusdm, bingx, bit2c, bitbank, bitbay, bitbns, bitcoincom, bitfinex, bitfinex2, bitflyer, bitget, bithumb, bitmart, bitmex, bitopro, bitpanda, bitrue, bitso, bitstamp, bitteam, bitvavo, bl3p, blockchaincom, blofin, btcalpha, btcbox, btcmarkets, btcturk, bybit, cex, coinbase, coinbaseinternational, coinbasepro, coincheck, coinex, coinlist, coinmate, coinmetro, coinone, coinsph, coinspot, cryptocom, currencycom, delta, deribit, digifinex, exmo, fmfwio, gate, gateio, gemini, hitbtc, hitbtc3, hollaex, htx, huobi, huobijp, hyperliquid, idex, independentreserve, indodax, kraken, krakenfutures, kucoin, kucoinfutures, kuna, latoken, lbank, luno, lykke, mercado, mexc, ndax, novadax, oceanex, okcoin, okx, onetrading, p2b, paymium, phemex, poloniex, poloniexfutures, probit, timex, tokocrypto, tradeogre, upbit, wavesexchange, wazirx, whitebit, woo, yobit, zaif, zonda, };
export default ccxt;
