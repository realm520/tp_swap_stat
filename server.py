import datetime
import copy
from fastapi import FastAPI, Path
from sqlalchemy.sql import func
from typing import Optional
from libs import Session
#from libs.models import StSwapKdata1Min, StSwapKdata5Min, StSwapKdata15Min, \
    #StSwapKdata30Min, StSwapKdataDaily, StSwapKdata6Hour, StSwapKdataWeekly, \
    #StSwapKdata1Hour, StSwapKdata2Hour, StSwapKdata12Hour, \
    #StSwapKdataMonthly
from libs.models import kline_table_list
from libs.models import StSwapLiquidity, StSwapKdataDaily, StSwapKdataWeekly
from libs.xt_api import Api


app = FastAPI()


@app.get("/swap_stat/trade_amount/{cycle}")
def get_trade_amount(cycle: str = Path(..., regex="^(daily|weekly)$")):
    session = Session()
    if cycle == 'daily':
        data = session.query(StSwapKdataDaily.timestamp,func.sum(StSwapKdataDaily.volume).label("volume")).group_by(StSwapKdataDaily.timestamp).all()
    elif cycle == 'weekly':
        data = session.query(StSwapKdataWeekly.timestamp,func.sum(StSwapKdataWeekly.volume).label("volume")).group_by(StSwapKdataWeekly.timestamp).all()
    xt_api = Api("", "")
    xwcPrice = xt_api.get_ticker(f'xwc_usdt')['price']
    result = []
    for d in data:
        result.append({'stat_time': d.timestamp, 'trade_amount': float(d.volume)*xwcPrice})
    session.close()
    return result


@app.get("/swap_stat/liquidity/{ex_pair}")
def get_liquidity(ex_pair: str = Path(..., regex="^(xwc_eth|xwc_tp|xwc_cusd|all)$")):
    session = Session()
    if ex_pair == 'all':
        data = session.query(StSwapLiquidity).order_by(StSwapLiquidity.stat_time).all()
    else:
        data = session.query(StSwapLiquidity).\
                filter(StSwapLiquidity.tp_name==ex_pair).\
                order_by(StSwapLiquidity.stat_time).all()
    liquidity = []
    xt_api = Api("", "")
    price = {
        'XWC': xt_api.get_ticker(f'xwc_usdt')['price'],
        'ETH': xt_api.get_ticker(f'eth_usdt')['price'],
        'TP': xt_api.get_ticker(f'tp_usdt')['price'],
        'CUSD': 1
    }
    print(price)
    dailyData = {
        "stat_time": 0,
        "market_value": -1
    }
    for d in data:
        if dailyData['stat_time'] == d.stat_time:
            dailyData['market_value'] +=  d.token1_amount / 10 ** 8 * price[d.token1_name] + d.token2_amount / 10 ** 8 * price[d.token2_name]
        else:
            if dailyData['stat_time'] != 0:
                while dailyData['stat_time'] != d.stat_time:
                    liquidity.append(copy.deepcopy(dailyData))
                    print(dailyData)
                    dailyData['stat_time'] += datetime.timedelta(days=1)
            dailyData['stat_time'] = d.stat_time
            dailyData['market_value'] =  d.token1_amount / 10 ** 8 * price[d.token1_name] + d.token2_amount / 10 ** 8 * price[d.token2_name]
    liquidity.append(copy.deepcopy(dailyData))
    session.close()
    return liquidity


@app.get("/swap_stat/kline/{ex_pair}/{k_type}")
def get_kline(ex_pair: str = Path(..., regex="^(xwc_eth|xwc_tp|xwc_cusd)$"), k_type: int = Path(0, ge=0, lt=11), limit: int = 100):
    session = Session()
    if k_type < 0 or k_type >= len(kline_table_list):
        print(f"invalid k_type [MUST between 0 - {len(kline_table_list)-1}]")
        return f"invalid k_type [MUST between 0 - {len(kline_table_list)-1}]"
    cycles = [60, 300, 900, 1800, 3600, 7200, 21600, 43200, 86400, 604800, 2592000]
    k_table = kline_table_list[k_type]
    #print(k_table, ex_pair)
    now = datetime.datetime.utcnow()
    start = now - datetime.timedelta(seconds=(limit*cycles[k_type]+1))
    print(start.strftime("%Y-%m-%d %H:%M:%S"))
    missing_position = 0
    try:
        data = session.query(k_table).filter(k_table.ex_pair==ex_pair, k_table.timestamp>=start).\
            order_by(k_table.timestamp).all()
    except Exception as e:
        print(str(e))
        return []
    if len(data) == 0:
        data = session.query(k_table).filter(k_table.ex_pair==ex_pair).\
            order_by(k_table.timestamp.desc()).limit(1).all()
        if len(data) == 1:
            data[0].volume = 0
            data[0].block_num = 0
    else:
        missing_position = len(data)
    if data is None or len(data) == 0:
        return []
    last_item = copy.deepcopy(data[len(data)-1])
    last_item.volume = 0
    last_item.block_num = 0
    last_item.k_open = last_item.k_close
    last_item.k_high = last_item.k_close
    last_item.k_low = last_item.k_close
    while True:
        last_item.timestamp += datetime.timedelta(seconds=cycles[k_type])
        if last_item.timestamp > now:
            break
    if missing_position == 0:
        data = []
    for i in range(missing_position, limit):
        # logging.info(last_item.timestamp)
        last_item.timestamp -= datetime.timedelta(seconds=cycles[k_type])
        if missing_position > 0 and last_item.timestamp <= data[missing_position-1].timestamp:
            break
        else:
            data.insert(missing_position, copy.deepcopy(last_item))
    session.close()
    return data


#@app.get("/items/{item_id}")
#def read_item(item_id: int, q: str = None):
    #return {"item_id": item_id, "q": q}
