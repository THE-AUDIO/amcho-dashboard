from core.bd import get_db_session, engine
from core.base import Base
from load.loader import BaseLoader
from extract.extractor import extract_cocoa, extract_ppi
from transform.transformer import transform_cocoa, transform_ppi
from model.cocoa import CocoaPrice
from model.ppi import PPI
from model.users import users

def init_db():
    Base.metadata.create_all(engine)
    print("DB initialized")
    
def run():
    print("Starting ETL process...")
    get_db_session()
    init_db()
    cocoa_df = extract_cocoa()
    ppi_df = extract_ppi()
    transformed_cocoa = transform_cocoa(cocoa_df)
    transformed_ppi = transform_ppi(ppi_df)
    print(transformed_cocoa)
    print(transformed_ppi)
    loader = BaseLoader(engine)
    loader.replace_table("cocoa_price", transformed_cocoa)
    loader.replace_table("ppi", transformed_ppi)
    print("ETL process completed successfully")

if __name__=="__main__":
    
    run()