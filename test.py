import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# เชื่อมต่อฐานข้อมูล
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="mydb"  # เปลี่ยนเป็นชื่อฐานข้อมูลของคุณ
)
