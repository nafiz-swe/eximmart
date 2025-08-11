
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # তোমার MySQL পাসওয়ার্ড নাই বলেছিলে, তাই ফাঁকা
        database="eximmartdb"
    )
