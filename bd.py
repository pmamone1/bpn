import pymysql
import mysql.connector

def db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='pablo1612',
                           db='bpn') 
    