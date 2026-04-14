import pymysql
from dbutils.pooled_db import PooledDB
POOL=PooledDB(
    creator=pymysql,#模块
    maxconnections=10,#允许的最大链接数
    mincached=2,#初始化时最少的空闲链接
    maxcached=5,#最多闲置链接
    blocking=True,#无可用链接后是否等待
    setsession=[],#开始会话前执行的sql指令列表
    ping=0,#延迟
    host='127.0.0.1',
    port=3306,
    user='root',
    password='1212334',
    db='project2',
    charset='utf8'
)
def fetch_one(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result
def mysql_caozuo(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor()
    cursor.execute(sql,params)
    conn.commit()
    cursor.close()
    conn.close()
    return 1
def fetch_all(sql,params):
    conn=POOL.connection()
    cursor=conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(sql,params)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def insert_and_get_id(sql, params):
    conn = POOL.connection()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    # 获取最后插入的ID
    last_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return last_id