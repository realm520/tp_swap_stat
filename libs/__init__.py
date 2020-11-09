from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine("mysql+pymysql://root:12PV1Kjlh@192.168.0.209/xwc_explorer", encoding="utf-8")
Session = sessionmaker(bind=engine)
session = Session()
