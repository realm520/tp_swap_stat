from . import Base
from sqlalchemy import Column, Integer, BigInteger, DateTime, String, Numeric, Text


class BlBlock(Base):
    __tablename__ = 'bl_block'
    block_num = Column(BigInteger, primary_key=True)
    block_time = Column(DateTime)

    def __init__(self, **kwargs):
        super(BlBlock, self).__init__(**kwargs)


class BlTxEvents(Base):
    __tablename__ = 'bl_tx_events'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    trx_id = Column(String(100), index=True)
    block_num = Column(Integer)
    op_num = Column(Integer)
    caller_addr = Column(String(100))
    contract_address = Column(String(100))
    event_name = Column(String(100))
    event_arg = Column(Text)
    event_seq = Column(Integer)

    def __init__(self, **kwargs):
        super(BlTxEvents, self).__init__(**kwargs)

    def __repr__(self):
        return '<BlTxEvents %r>' % self.tx_id
    
    def toQueryObj(self):
        return {"trx_id": self.trx_id, "caller_addr": self.caller_addr, \
                "contract_address": self.contract_address, "block_num": self.block_num, \
                "event_name": self.event_name}


class StSwapTick(Base):
    __tablename__ = 'st_swap_tick'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    ex_pair = Column(String(64), index=True)
    buy_asset = Column(String(32), index=True)
    sell_asset = Column(String(32), index=True)
    buy_amount = Column(Numeric(20, 8), nullable=False)
    sell_amount = Column(Numeric(20, 8), nullable=False)
    fee = Column(Numeric(20, 8), nullable=False)
    block_num = Column(BigInteger)
    price = Column(Numeric(20, 8), nullable=False)
    volume = Column(Numeric(20, 8), nullable=False)

    def __init__(self, **kwargs):
        super(StSwapTick, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapTick %r>' % self.tx_id
    
    def toQueryObj(self):
        return {"pair": self.ex_pair, "price": self.price, \
                "volume": self.volume, "block_num": self.block_num, \
                "timestamp": self.timestamp}


class StSwapKdata1Min(Base):
    __tablename__ = 'st_swap_kdata_1min'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20,8))
    k_close = Column(Numeric(20,8))
    k_low = Column(Numeric(20,8))
    k_high = Column(Numeric(20,8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata1Min, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata1Min %r>' % self.tx_id
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata5Min(Base):
    __tablename__ = 'st_swap_kdata_5min'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata5Min, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata5Min %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata15Min(Base):
    __tablename__ = 'st_swap_kdata_15min'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata15Min, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata15Min %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.e, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata30Min(Base):
    __tablename__ = 'st_swap_kdata_30min'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata30Min, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata30Min %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata1Hour(Base):
    __tablename__ = 'st_swap_kdata_1hour'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata1Hour, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata1Hour %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata2Hour(Base):
    __tablename__ = 'st_swap_kdata_2hour'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata2Hour, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata2Hour %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata6Hour(Base):
    __tablename__ = 'st_swap_kdata_6hour'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata6Hour, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata6Hour %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdata12Hour(Base):
    __tablename__ = 'st_swap_kdata_12hour'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdata12Hour, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdata12Hour %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdataDaily(Base):
    __tablename__ = 'st_swap_kdata_daily'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdataDaily, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdataDaily %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdataWeekly(Base):
    __tablename__ = 'st_swap_kdata_weekly'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20,8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdataWeekly, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdataWeekly %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


class StSwapKdataMonthly(Base):
    __tablename__ = 'st_swap_kdata_monthly'
    id = Column(Integer, primary_key=True)
    ex_pair = Column(String(64), index=True)
    k_open = Column(Numeric(20, 8))
    k_close = Column(Numeric(20, 8))
    k_low = Column(Numeric(20, 8))
    k_high = Column(Numeric(20, 8))
    volume = Column(Numeric(20, 8))
    block_num = Column(Integer)
    timestamp = Column(DateTime)

    def __init__(self, **kwargs):
        super(StSwapKdataMonthly, self).__init__(**kwargs)

    def __repr__(self):
        return '<StSwapKdataMonthly %r>' % self.block_num
    
    def toQueryObj(self):
        return {"ex_pair": self.ex_pair, "k_open": self.k_open, "k_close": self.k_close, "k_low": self.k_low, \
                "k_high": self.k_high, \
                "volume": self.volume, "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}


kline_table_list = [
    StSwapKdata1Min, 
    StSwapKdata5Min,
    StSwapKdata15Min,
    StSwapKdata30Min,
    StSwapKdata1Hour,
    StSwapKdata2Hour,
    StSwapKdata6Hour,
    StSwapKdata12Hour,
    StSwapKdataDaily,
    StSwapKdataWeekly,
    StSwapKdataMonthly
]
