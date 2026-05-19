from core.bd import get_db_session, engine
from core.base import Base
from load.loader import BaseLoader
from extract.extractor import extract_cocoa, extract_ppi
from transform.transformer import transform_cocoa, transform_ppi
from model.cocoa import CocoaPrice
from model.ppi import PPI

def init_db():
    Base.metadata.create_all(engine)
    print("DB initialized")
    
def run():
    get_db_session()
    init_db()
    cocoa_df = extract_cocoa()
    ppi_df = extract_ppi()
    # transformed_cocoa = transform_cocoa(cocoa_df)
    # transformed_ppi = transform_ppi(ppi_df)
    loader = BaseLoader(engine)
    loader.replace_table("cocoa_price", cocoa_df)
    loader.replace_table("ppi", ppi_df)

if __name__=="__main__":
    
    run()