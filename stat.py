#coding=utf-8

import json
import time
import datetime
import pymysql
from sqlalchemy import func
from libs.xwc_api import XWC
from libs.xt_api import Api
from libs import session
from libs.models import StSwapTick, BlTxEvents, BlBlock


class TokenSwapStat:
    def __init__(self, xwc_api, xt_api):
        self._xwc_api = xwc_api
        self._xt_api = xt_api
        self.pairs = {
            'xwc_eth': 'XWCCJV5jJ8acWx3AfVPUT6x1K2hXRkptZ8hGB',
            'xwc_cusd': 'XWCCarrfVrHCRupUbJfasasx2Rdy4Aor8eTD9',
            'xwc_tp': 'XWCCcUF3uQDHzyhAuKsZ9DtFyVBcFuousjR6w'
        }
        self.id2AssetName = {'1.3.0': 'XWC', '1.3.3': 'ETH'}
        self.last1HourBlock = 0
        self.last24HourBlock = 0
        self.firstTpBlock = 5003249
        self.perBlockTp = 0.06944444

    def addr2Token(self, address):
        originAssets = ['XWC', 'ETH']
        addrTokenMap = {
            'XWCCUXT5Dr5EdYtoHBkCsTqSUUEpNd5uf22Db': 'TP',
            'XWCCc55NYwUDeQyy2Co5hqdFt75wWUrMu71rW': 'CUSD',
            'XWC': 'XWC',
            'ETH': 'ETH'
        }
        if address in originAssets:
            return address
        else:
            return addrTokenMap[address]

    def _getMatchedBlock(self, startBlock, endBlock, startTime):
        blockNumber = startBlock
        while blockNumber < endBlock:
            block = self._xwc_api.get_block(blockNumber)
            blockTime = int(time.mktime(time.strptime(block['timestamp'], "%Y-%m-%dT%H:%M:%S")))
            if startTime < blockTime:
                return blockNumber - 1
            blockNumber += 1
        return 0

    def _getBatch2Reward(self, startBlock, endBlock, totalReward):
        perWeekBlock = 7 * 24 * 600
        weekBlocks = [[5360500+perWeekBlock*i, totalReward/16*(2-i)*5/perWeekBlock] for i in range(3)]
        weekBlocks[2][1] = totalReward/16/perWeekBlock
        reward = 0

        for b in weekBlocks:
            if startBlock > b[0]+perWeekBlock or endBlock < b[0]:
                continue
            if startBlock >= b[0]:
                segStart = startBlock
            else:
                segStart = b[0]
            if endBlock >= b[0]+perWeekBlock:
                segEnd = b[0]+perWeekBlock
            else:
                segEnd = endBlock
            reward += (segEnd-segStart) * b[1]
        return reward

    def tpStat(self, address):
        currentHeight = self._xwc_api.get_block_height()
        currentTime = int(time.time()) - 28800 # convert to UTC timestamp
        #block = self._xwc_api.get_block(5190601)
        #blockTime = int(time.mktime(time.strptime(block['timestamp'], "%Y-%m-%dT%H:%M:%S")))
        #print(blockTime)
        #print(currentTime-blockTime)
        #return
        temp24HourHeight = self.last24HourBlock if self.last24HourBlock > 0 else currentHeight - 14400
        temp1HourHeight = self.last1HourBlock if self.last1HourBlock > 0 else currentHeight - 600
        self.last24HourBlock = self._getMatchedBlock(temp24HourHeight, currentHeight, currentTime-86400)
        self.last1HourBlock = self._getMatchedBlock(temp1HourHeight, currentHeight, currentTime-3600)
        tpStat = {}
        if self.last24HourBlock > 0 and self.last1HourBlock > 0:
            if address == 'XWCCJV5jJ8acWx3AfVPUT6x1K2hXRkptZ8hGB':
                tpStat['tp1Hour'] = (currentHeight - self.last1HourBlock) * self.perBlockTp
                tpStat['tp24Hour'] = (currentHeight - self.last24HourBlock) * self.perBlockTp
                tpStat['tpSupply'] = (currentHeight - self.firstTpBlock) * self.perBlockTp
                if tpStat['tpSupply'] > 30000:
                    tpStat['tpSupply'] = 30000
                    tpStat['tp1Hour'] = 0
                    tpStat['tp24Hour'] = 0
            elif address == 'XWCCarrfVrHCRupUbJfasasx2Rdy4Aor8eTD9':
                tpStat['tp1Hour'] = self._getBatch2Reward(self.last1HourBlock, currentHeight, 20000)
                tpStat['tp24Hour'] = self._getBatch2Reward(self.last24HourBlock, currentHeight, 20000)
                tpStat['tpSupply'] = self._getBatch2Reward(5360500, currentHeight, 20000)
                if tpStat['tpSupply'] > 20000:
                    tpStat['tpSupply'] = 20000
                    tpStat['tp1Hour'] = 0
                    tpStat['tp24Hour'] = 0
            elif address == 'XWCCcUF3uQDHzyhAuKsZ9DtFyVBcFuousjR6w':
                tpStat['tp1Hour'] = self._getBatch2Reward(self.last1HourBlock, currentHeight, 50000)
                tpStat['tp24Hour'] = self._getBatch2Reward(self.last24HourBlock, currentHeight, 50000)
                tpStat['tpSupply'] = self._getBatch2Reward(5360500, currentHeight, 50000)
                if tpStat['tpSupply'] > 50000:
                    tpStat['tpSupply'] = 50000
                    tpStat['tp1Hour'] = 0
                    tpStat['tp24Hour'] = 0
        return tpStat

    def swapStat(self, address, token1, token2):
        data = {
                #'fee': { token2: 0, token1: 0 },
                'rate1Day': { token2: 0, token1:0 },
                'pool': { token2: 0, token1: 0 },
                'price': { token2: 0, token1: 0 }
                }
        ticker = self._xt_api.get_ticker(f'{token1.lower()}_usdt')
        data['rate1Day'][token1] = f"{ticker['rate']}"
        data['price'][token1] = ticker['price']
        if token2 != 'CUSD':
            ticker = self._xt_api.get_ticker(f'{token2.lower()}_usdt')
            data['rate1Day'][token2] = f"{ticker['rate']}"
            data['price'][token2] = ticker['price']
        else:
            data['rate1Day'][token2] = 0
            data['price'][token2] = 1
        info = self._xwc_api.get_depth(f'{token1.lower()}_{token2.lower()}')
        if info is None:
            return
        print(info['token_1_contractAddr'], token1, self.addr2Token(info['token_1_contractAddr']))
        if info['token_1_contractAddr'] == token1 or token1 == self.addr2Token(info['token_1_contractAddr']):
            data['pool'][token1] = f"{info['token_1_pool_amount']/10**8:>.4f}"
            data['pool'][token2] = f"{info['token_2_pool_amount']/10**8:>.4f}"
        else:
            data['pool'][token2] = f"{info['token_1_pool_amount']/10**8:>.4f}"
            data['pool'][token1] = f"{info['token_2_pool_amount']/10**8:>.4f}"
        print(f"{token2}: {info['token_1_pool_amount']/10**8:>.4f}, {token1}: {info['token_2_pool_amount']/10**8:>.4f}")
 
        db = pymysql.connect(host="192.168.0.209",
                     user="root",
                     password="12PV1Kjlh",
                     port=3306,
                     database="xwc_explorer",
                     charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("select min(block_num) from bl_block where block_time > date_sub(now(), interval 1 DAY)")
            results = cursor.fetchall()
            block1Day = results[0][0]
            cursor.execute("select min(block_num) from bl_block where block_time > date_sub(now(), interval 7 DAY)")
            results = cursor.fetchall()
            block7Day = results[0][0]
        except:
            return
        txCount = 0
        # all days
        try:
            exData = {'exchange': {token2: 0, token1: 0}, 'fee': {token2: 0, token1: 0}}
            ex1DayData = {'exchange': {token2: 0, token1: 0}, 'fee': {token2: 0, token1: 0}}
            ex7DaysData = {'exchange': {token2: 0, token1: 0}, 'fee': {token2: 0, token1: 0}}
            cursor.execute(f"select event_arg,block_num from bl_tx_events where contract_address = '{address}' and event_name='Exchanged'")
            results = cursor.fetchall()
            for row in results:
                txCount += 1
                exchange = json.loads(row[0])
                exchange['buy_asset'] = self.addr2Token(exchange['buy_asset'])
                exchange['sell_asset'] = self.addr2Token(exchange['sell_asset'])
                exData['fee'][exchange['sell_asset']] += exchange['fee']
                exData['exchange'][exchange['buy_asset']] += exchange['buy_amount']
                exData['exchange'][exchange['sell_asset']] += exchange['sell_amount']
                if row[1] > block1Day:
                    ex1DayData['fee'][exchange['sell_asset']] += exchange['fee']
                    ex1DayData['exchange'][exchange['buy_asset']] += exchange['buy_amount']
                    ex1DayData['exchange'][exchange['sell_asset']] += exchange['sell_amount']
                if row[1] > block7Day:
                    ex7DaysData['fee'][exchange['sell_asset']] += exchange['fee']
                    ex7DaysData['exchange'][exchange['buy_asset']] += exchange['buy_amount']
                    ex7DaysData['exchange'][exchange['sell_asset']] += exchange['sell_amount']
            exData['exchange'][token2] = f"{exData['exchange'][token2]/10**8:>.4f}"
            exData['exchange'][token1] = f"{exData['exchange'][token1]/10**8:>.4f}"
            exData['fee'][token2] = f"{exData['fee'][token2]/10**8:>.4f}"
            exData['fee'][token1] = f"{exData['fee'][token1]/10**8:>.4f}"
            ex1DayData['exchange'][token2] = f"{ex1DayData['exchange'][token2]/10**8:>.4f}"
            ex1DayData['exchange'][token1] = f"{ex1DayData['exchange'][token1]/10**8:>.4f}"
            ex1DayData['fee'][token2] = f"{ex1DayData['fee'][token2]/10**8:>.4f}"
            ex1DayData['fee'][token1] = f"{ex1DayData['fee'][token1]/10**8:>.4f}"
            ex7DaysData['exchange'][token2] = f"{ex7DaysData['exchange'][token2]/10**8:>.4f}"
            ex7DaysData['exchange'][token1] = f"{ex7DaysData['exchange'][token1]/10**8:>.4f}"
            ex7DaysData['fee'][token2] = f"{ex7DaysData['fee'][token2]/10**8:>.4f}"
            ex7DaysData['fee'][token1] = f"{ex7DaysData['fee'][token1]/10**8:>.4f}"
            data['allDay'] = exData
            data['1day'] = ex1DayData
            data['7day'] = ex7DaysData
        except Exception as e:
            print(str(e))
            pass
        data['txCount'] = txCount
        data['tpStat'] = self.tpStat(address)
        print(json.dumps(data))
        return data

    def _updateSinglePair(self, address, start_block_num, ex_pair):
        precision = 10 ** 8
        try:
            #cursor.execute(f"select event_arg,block_num from bl_tx_events where contract_address = '{address}' and event_name='Exchanged' and block_num > {start_block_num}")
            #results = cursor.fetchall()
            results = session.query(BlTxEvents.event_arg,BlTxEvents.block_num). \
                filter(
                        BlTxEvents.contract_address==address,
                        BlTxEvents.event_name=='Exchanged',
                        BlTxEvents.block_num>start_block_num).\
                all()
            lastBlockTime = 0
            lastBlockNum = 0
            for r in results:
                exchange = json.loads(r[0])
                exchange['buy_asset'] = self.addr2Token(exchange['buy_asset'])
                exchange['sell_asset'] = self.addr2Token(exchange['sell_asset'])
                if exchange['buy_asset'] == 'XWC':
                    price = exchange['sell_amount'] / exchange['buy_amount']
                    volume = exchange['buy_amount'] / precision
                elif exchange['sell_asset'] == 'XWC':
                    price = exchange['buy_amount'] / exchange['sell_amount']
                    volume = exchange['sell_amount'] / precision
                else:
                    price = 0
                    volume = 0
                exchange['buy_amount'] = exchange['buy_amount'] / precision
                exchange['sell_amount'] = exchange['sell_amount'] / precision
                exchange['fee'] = exchange['fee'] / precision
                if lastBlockNum == 0 or lastBlockNum != r[1]:
                    block = session.query(BlBlock.block_time).filter(BlBlock.block_num==r[1]).first()
                    lastBlockNum = r[1]
                    lastBlockTime = block.block_time
                session.add(StSwapTick(
                    timestamp=lastBlockTime,
                    ex_pair=ex_pair,
                    buy_asset=exchange['buy_asset'],
                    sell_asset=exchange['sell_asset'],
                    buy_amount=exchange['buy_amount'],
                    sell_amount=exchange['sell_amount'],
                    fee=exchange['fee'],
                    block_num=lastBlockNum,
                    price=price,
                    volume=volume
                ))
        except Exception as e:
            print(str(e))
            return
 

    def updateTick(self):
        last_tick = session.query(func.max(StSwapTick.block_num).label('block_num')).first()
        if last_tick.block_num is None:
            print("first time")
            start_block_num = 4992608
        else:
            start_block_num = int(last_tick.block_num)
        print(f'update tick - start block: {start_block_num}')
        for k, v in self.pairs.items():
            self._updateSinglePair(v, start_block_num, k)
        session.commit()
        print('tick updated')

    def updateKline(self):
        from libs.models import StSwapKdata1Min, StSwapKdata5Min, StSwapKdata15Min, \
            StSwapKdata30Min, StSwapKdataDaily, StSwapKdata6Hour, StSwapKdataWeekly, \
            StSwapKdata1Hour, StSwapKdata2Hour, StSwapKdata12Hour, \
            StSwapKdataMonthly
        from libs.k_line_obj import KLine1MinObj, KLine5MinObj, KLine15MinObj, KLine30MinObj, KLine1HourObj, KLine2HourObj, \
                        KLine6HourObj, KLine12HourObj, KLineWeeklyObj, KLineDailyObj, KLineMonthlyObj
        def process_kline_common(base_table, target_table, process_obj, pair):
            print("base: %s, target: %s, pair: %s" % (str(base_table), str(target_table), pair))
            k_last = session.query(target_table).filter(target_table.ex_pair==pair).order_by(target_table.timestamp.desc()).limit(1).first()
            k = process_obj(k_last)
            if k_last is None:
                # if str(base_table) == "<class 'app.models.StSwapTick'>":
                last_time = datetime.datetime.utcnow() - datetime.timedelta(days=365)
            else:
                last_time = k_last.timestamp
            print("last time: %s" % (last_time))
            ticks = session.query(base_table).filter(base_table.ex_pair==pair, base_table.timestamp>=last_time).order_by(base_table.id).all()
            for t in ticks:
                k.process_tick(t)
            for r in k.get_k_data():
                if k_last is not None and k_last.timestamp == r['start_time']:
                    session.query(target_table).filter_by(timestamp=k_last.timestamp, ex_pair=pair).delete()
                session.add(target_table(ex_pair=pair, k_open=r['k_open'], k_close=r['k_close'], \
                    k_high=r['k_high'], k_low=r['k_low'], timestamp=r['start_time'], \
                    block_num=r['block_num'], volume=r['volume']))

        for p in self.pairs.keys():
            # Process 1-minute K-Line
            process_kline_common(StSwapTick, StSwapKdata1Min, KLine1MinObj, p)
            # Process 5-minutes K-Line
            process_kline_common(StSwapKdata1Min, StSwapKdata5Min, KLine5MinObj, p)
            # Process 15-minutes K-Line
            process_kline_common(StSwapKdata1Min, StSwapKdata15Min, KLine15MinObj, p)
            # Process 30-minutes K-Line
            process_kline_common(StSwapKdata1Min, StSwapKdata30Min, KLine30MinObj, p)
            # Process 1-hour K-Line
            process_kline_common(StSwapKdata1Min, StSwapKdata1Hour, KLine1HourObj, p)
            # Process 2-hour K-Line
            process_kline_common(StSwapKdata1Hour, StSwapKdata2Hour, KLine2HourObj, p)
            # Process 6-hour K-Line
            process_kline_common(StSwapKdata1Hour, StSwapKdata6Hour, KLine6HourObj, p)
            # Process 12-hour K-Line
            process_kline_common(StSwapKdata1Hour, StSwapKdata12Hour, KLine12HourObj, p)
            # Process daily K-Line
            process_kline_common(StSwapKdata1Hour, StSwapKdataDaily, KLineDailyObj, p)
            # Process weekly K-Line
            process_kline_common(StSwapKdata1Hour, StSwapKdataWeekly, KLineWeeklyObj, p)
            # Process monthly K-Line
            process_kline_common(StSwapKdataDaily, StSwapKdataMonthly, KLineMonthlyObj, p)
        session.commit()


    def stat(self):
        data = {}
        for k, v in self.pairs.items():
            pairs = k.split('_')
            data[k] = self.swapStat(v, pairs[0].upper(), pairs[1].upper())
        json.dump(data, open('/var/www/html/tokenswap_stat.json', 'w'))
        #json.dump(data, open('tokenswap_stat.json', 'w'))


if __name__ == '__main__':
    xwc_api = XWC('http://localhost:10044/api', 'caller0')
    xt_api = Api("", "")
    statObj = TokenSwapStat(xwc_api, xt_api)
    while True:
        try:
            statObj.stat()
            statObj.updateTick()
            statObj.updateKline()
        except Exception as e:
            print(str(e))
        time.sleep(6)
    #statObj.tpStat()
