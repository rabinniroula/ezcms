import sqlalchemy
from dotenv import load_dotenv
import os

load_dotenv()

user = os.getenv('DB_USER')
pwd  = os.getenv('DB_PASS')

engine = sqlalchemy.create_engine(f"mysql://{user}:{pwd}@localhost/ezcms")
conn = engine.connect()

def runQuery(query: str) -> list :
    try:
        res = conn.execute(sqlalchemy.sql.text(query))
    except sqlalchemy.exc.ProgrammingError:
        return ["error"]
    return res.fetchall()