import sqlite3

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect(db_path:str="./chronodash.db", return_dict:bool = False):
    con = sqlite3.connect(db_path)
    if return_dict:
        con.row_factory = _dict_factory
    cur = con.cursor()
    return con, cur

def fetch(sql:str):
    con, cur = connect(return_dict=True)
    cur.execute(sql)
    result = cur.fetchall()
    con.close()
    return result

def query(sql:str, params=None, commit=False):
    con, cur = connect()
    if params is None:
        cur.execute(sql)
    else:
        cur.execute(sql, params)
    if commit:
        con.commit()
    con.close()