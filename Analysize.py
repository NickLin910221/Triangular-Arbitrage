 # -*- coding: utf-8 -*-
import _thread
import datetime
import hashlib
import hmac
import json

import loguru
import requests
import websocket
from binance.client import Client

import LineNotify as Notify

#Line_Notify_Token
Line_Notify_Token = ""

### TESTNET
#api_url = "https://testnet.binance.vision/api/v3"
#api_key = ""
#secret = ""

### MANINET
api_url = ""
api_key = ""
secret = ""
client = Client(api_key,secret)

file_name = "config.json"
with open(file_name, "r") as f:
    data = json.load(f)
    api_url = data["url"]
    api_key = data["api_key"]
    secret  = data["api_secret"]
    Line_Notify_Token = data["Line_token"]

loguru.logger.add(str(datetime.date.today().strftime("%Y%m%d")) + '  profit.log',rotation='10MB' ,retention="7 days" ,level="DEBUG")

### Parameter
trade_positive_times = 0
trade_opposite_times = 0
fee_rate = 0.0006
basic_fee = pow(float(1)-fee_rate,3)
class_name = 0

class data():
    def __init__(self, **kwargs):
        # Simple a : ADA, b : btc, c : USDT
        self.a, self.b, self.c = kwargs["a"], kwargs["b"], kwargs["c"] 
        self.pair1, self.pair2, self.pair3 = self.a + self.c, self.b + self.c, self.a + self.b
        self.a_bid_price, self.a_bid_volume, self.a_ask_price, self.a_ask_volume = 0, 0, 0, 0
        self.b_bid_price, self.b_bid_volume, self.b_ask_price, self.b_ask_volume = 0, 0, 0, 0
        self.c_bid_price, self.c_bid_volume, self.c_ask_price, self.c_ask_volume = 0, 0, 0, 0

    def var(self, **kwargs):
        if kwargs['pair'] == 'a':
            self.a_bid_price, self.a_bid_volume, self.a_ask_price, self.a_ask_volume = float(kwargs['a_bid_price']), float(kwargs['a_bid_volume']), float(kwargs['a_ask_price']), float(kwargs['a_ask_volume'])
        if kwargs['pair'] == 'b': 
            self.b_bid_price, self.b_bid_volume, self.b_ask_price, self.b_ask_volume = float(kwargs['b_bid_price']), float(kwargs['b_bid_volume']), float(kwargs['b_ask_price']), float(kwargs['b_ask_volume'])
        if kwargs['pair'] == 'c':
            self.c_bid_price, self.c_bid_volume, self.c_ask_price, self.c_ask_volume = float(kwargs['c_bid_price']), float(kwargs['c_bid_volume']), float(kwargs['c_ask_price']), float(kwargs['c_ask_volume'])

    def accountbalance(self, asset):
        pass
        #TODO : use pass to avoid the api requests too frequently
        #       diabled the following todo will have the real take-order function 
        #       Please cautious the risk 

        #try:
        #    return client.get_asset_balance(asset=asset)['free']
        #except Exception as error:
        #    print(error)

    def calculate(self):
        try:
            positive = round(1/float(self.a_ask_price)/float(self.b_ask_price)*float(self.c_bid_price),5)
            opposite = round(1/float(self.c_ask_price)*float(self.b_bid_price)*float(self.a_bid_price),5)
            if positive > (1/basic_fee):
                ### trigger position trade
                capacity = min(self.a_ask_price*self.a_ask_volume,self.b_ask_price*self.b_ask_volume*self.a_ask_price,self.c_bid_price*self.c_bid_volume)
                loguru.logger.info(trade.create_order(self.pair2.upper(), "BUY", "LIMIT", "FOK", min(capacity,self.accountbalance(self.c)), self.a_ask_price))
                loguru.logger.info(trade.create_order(self.pair3.upper(), "BUY", "LIMIT", "FOK", min(capacity,self.accountbalance(self.b)), self.b_ask_price))
                loguru.logger.info(trade.create_order(self.pair1.upper(), "SELL", "LIMIT", "FOK", min(capacity,self.accountbalance(self.a)), self.c_bid_price))
                Notify.SendMessageToLineNotify("Positive","")
                self.trade_positive_times += 1
            else:
                print(self.c + " -> " + self.b + " -> " + self.a + " Positive not trigger")
            if opposite > (1/basic_fee):
                ### trigger opposite trade
                capacity = min(self.c_ask_price*self.c_ask_volume,self.b_bid_price*self.b_bid_volume*self.a_bid_price,self.a_bid_price*self.a_bid_volume)
                loguru.logger.info(trade.create_order(self.pair1.upper(), "BUY", "LIMIT", "FOK", min(capacity, self.accountbalance(self.c)), self.c_ask_price))
                loguru.logger.info(trade.create_order(self.pair3.upper(), "BUY", "LIMIT", "FOK", min(capacity, self.accountbalance(self.a)), self.b_bid_price))
                loguru.logger.info(trade.create_order(self.pair2.upper(), "SELL", "LIMIT", "FOK", min(capacity, self.accountbalance(self.b)), self.a_bid_price))
                Notify.SendMessageToLineNotify("Opposite","l2EdidUvuUE1aiFoCC00WSHO48H0AXCdbcydPz4NPNy")
                self.trade_opposite_times += 1
            else:
                print(self.c + " -> " + self.a + " -> " + self.b + " pposite not trigger")
            print("#####\t" + "\tPOSITIVE\t" + str(positive) + "\t" + str(trade_positive_times) + "\tOPPOSITE\t" + str(opposite) + "\t" + str(trade_opposite_times) + "\t" + " \t#####")
        except ZeroDivisionError:
            pass

class trade():
    def HMAC_SHA256(appkey,strToSign):
        # HMAC_SHA256å 撖
        signature = hmac.new(bytes(appkey, encoding="utf-8"), bytes(strToSign, encoding="utf-8"), digestmod=hashlib.sha256).digest().hex().lower()
        return signature

    def create_order(symbol,side,markettype,timeInForce,quantity,price):
        # Ping ServerTime
        servertime = requests.get(api_url + "/api/v3/time")
        servertime = json.loads(servertime.text)['serverTime']
        # Generate Signature and order
        querystring = "symbol=" + symbol + "&side=" + side + "&type=" + markettype + "&timeInForce=" + timeInForce + "quantity=" + str(quantity) + "&price=" + str(price) + "&recvWindow=5000&timestamp=" + str(servertime)
        request_body = "symbol=" + symbol + "&side=" + side + "&type=" + markettype + "&timeInForce=" + timeInForce
        hashedsig = trade.HMAC_SHA256(secret,querystring)
        parameter = "quantity=" + str(quantity) + "&price=" + str(price) + "&recvWindow=5000&timestamp=" + str(servertime) + "&signature=" + hashedsig
        try:
            URL = requests.post(api_url + "/api/v3/order?" + request_body ,data = parameter, headers = {"X-MBX-APIKEY" : api_key})
            return URL.json()
        except error as error:
            loguru.logger.debug(error)
            print(error)

def on_open():
    print(" Connection is opened!")

def on_message(ws, message):
        jsLoads = json.loads(message)
        symbol  = jsLoads["data"]['s']
        for i in range(2):
            if symbol == globals()[i].pair1.upper():
                globals()[i].var(pair = 'a', 
                                            a_bid_price = float(jsLoads["data"]['b']), 
                                            a_bid_volume = float(jsLoads["data"]['B']), 
                                            a_ask_price = float(jsLoads["data"]['a']), 
                                            a_ask_volume = float(jsLoads["data"]['A']))
                print(globals()[i].a_bid_price,globals()[i].a_bid_volume,globals()[i].a_ask_price,globals()[i].a_ask_volume,globals()[i].b_bid_price,globals()[i].b_bid_volume,globals()[i].b_ask_price,globals()[i].b_ask_volume,globals()[i].c_bid_price,globals()[i].c_bid_volume,globals()[i].c_ask_price,globals()[i].c_ask_volume)
                globals()[i].calculate()
            if symbol == globals()[i].pair2.upper():
                globals()[i].var(pair = 'b', 
                                            b_bid_price = jsLoads["data"]['b'], 
                                            b_bid_volume = jsLoads["data"]['B'], 
                                            b_ask_price = jsLoads["data"]['a'], 
                                            b_ask_volume = jsLoads["data"]['A'])
                print(globals()[i].a_bid_price,globals()[i].a_bid_volume,globals()[i].a_ask_price,globals()[i].a_ask_volume,globals()[i].b_bid_price,globals()[i].b_bid_volume,globals()[i].b_ask_price,globals()[i].b_ask_volume,globals()[i].c_bid_price,globals()[i].c_bid_volume,globals()[i].c_ask_price,globals()[i].c_ask_volume)
                globals()[i].calculate()
            if symbol == globals()[i].pair3.upper():
                globals()[i].var(pair = 'c', 
                                            c_bid_price = jsLoads["data"]['b'], 
                                            c_bid_volume = jsLoads["data"]['B'], 
                                            c_ask_price = jsLoads["data"]['a'], 
                                            c_ask_volume = jsLoads["data"]['A'])
                print(globals()[i].a_bid_price,globals()[i].a_bid_volume,globals()[i].a_ask_price,globals()[i].a_ask_volume,globals()[i].b_bid_price,globals()[i].b_bid_volume,globals()[i].b_ask_price,globals()[i].b_ask_volume,globals()[i].c_bid_price,globals()[i].c_bid_volume,globals()[i].c_ask_price,globals()[i].c_ask_volume)
                globals()[i].calculate()

def ws_thread(**kwargs):
    ws = websocket.WebSocketApp(kwargs["url"], on_open = on_open, on_message = on_message, on_close= on_close)
    ws.run_forever()


def on_close():
    print(" Connection is closed! ")

def main(class_name, **kwargs):
    globals()[class_name] = data(a = kwargs['a'], b = kwargs['b'], c = kwargs['c'])
    print(globals()[class_name].b)
    socket = "wss://stream.binance.com/stream?streams=" + globals()[class_name].pair1 + "@bookTicker/" + globals()[class_name].pair2 + "@bookTicker/" + globals()[class_name].pair3 + "@bookTicker"
    print(socket)
    _thread.start_new_thread(ws_thread,(),{'url' : socket} )

if __name__ == "__main__":
    Notify.SendMessageToLineNotify("\n" + datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "\n Monitor Bot Start Up SUCCESS.", Line_Notify_Token)
    main()