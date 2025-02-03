import pymysql

connection = pymysql.connect(host='127.0.0.1', user='root', password='password1!', database='virtual_coin', charset='utf8mb4')
cur = connection.cursor(pymysql.cursors.DictCursor)

sql_SHOWTABLES = "show tables"
cur.execute(sql_SHOWTABLES)
resDB = cur.fetchall()

print(type(resDB))
print(resDB)