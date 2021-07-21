# import mysql.connector as mysqldb

# def mySqlDbGetAll(query):
#     mydb = mysqldb.connect(host='localhost', user='root', password='root', database='nkc')
#     mycursor = mydb.cursor()
#     mycursor.execute(query)
#     result = mycursor.fetchall()
#     mydb.close()
#     mycursor.close()
#     return result

# def mySqlDbGetAllByValue(query, val):
#     mydb = mysqldb.connect(host='localhost', user='root', password='root', database='nkc')
#     mycursor = mydb.cursor()
#     mycursor.execute(query, val)
#     result = mycursor.fetchall()
#     mydb.close()
#     mycursor.close()
#     return result

# def mySqlDbGetOneByValue(query, val):
#     mydb = mysqldb.connect(host='localhost', user='root', password='root', database='nkc')
#     mycursor = mydb.cursor()
#     mycursor.execute(query, val)
#     result = mycursor.fetchone()
#     mydb.close()
#     mycursor.close()
#     return result
