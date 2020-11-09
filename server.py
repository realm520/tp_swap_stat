import datetime
from fastapi import FastAPI, Path
from typing import Optional
from libs import Session
#from libs.models import StSwapKdata1Min, StSwapKdata5Min, StSwapKdata15Min, \
    #StSwapKdata30Min, StSwapKdataDaily, StSwapKdata6Hour, StSwapKdataWeekly, \
    #StSwapKdata1Hour, StSwapKdata2Hour, StSwapKdata12Hour, \
    #StSwapKdataMonthly
from libs.models import kline_table_list


app = FastAPI()


@app.get("/swap_stat/kline/{ex_pair}/{k_type}")
def get_kline(ex_pair: str = Path(..., regex="^(xwc_eth|xwc_tp|xwc_cusd)$"), k_type: int = Path(0, ge=0, lt=11), limit: int = 100):
    import copy
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