import pymysql

def create_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',  
        password='',  
        database='viticulture'  
    )
    return connection
