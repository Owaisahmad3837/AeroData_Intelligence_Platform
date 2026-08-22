from src.airport_data_platform.config.db_connection import (
    neon_db_connection,
    local_db_connection
)


print("LOCAL TEST")

local_conn=local_db_connection()

cur=local_conn.cursor()
cur.execute("select version()")

print(cur.fetchall())

cur.close()
local_conn.close()



print("NEON TEST")
neon_conn=neon_db_connection()

cur=neon_conn.cursor()
cur.execute("select version()")

print(cur.fetchall())

cur.close()
neon_conn.close()