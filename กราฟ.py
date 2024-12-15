import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# เชื่อมต่อฐานข้อมูล
connection = mysql.connector.connect(
    host="localhost",
    user="myuser",
    password="mypassword",
    database="mydb"  # เปลี่ยนเป็นชื่อฐานข้อมูลของคุณ
)


cursor = connection.cursor()

cursor.execute('''
SELECT
  THProvince,
  COUNT(*) AS ทั้งหมด,
  COUNT(CASE WHEN TitleName LIKE "%พระ%" THEN 1 END) AS Monk,
  COUNT(CASE WHEN SEX  LIKE '%ชาย%'  THEN 1 END) AS M,
  COUNT(CASE WHEN SEX  NOT LIKE '%ชาย%'  THEN 1 END) AS F
FROM
clinicvisit
WHERE
THProvince is not NULL
AND
Service_Date BETWEEN '2020-01-01' AND '2023-01-01'
GROUP BY
THProvince
 LIMIT 10''')

data = cursor.fetchall()

columns = [col[0] for col in cursor.description]
# สร้าง DataFrame จากข้อมูลที่ดึงมา
df = pd.DataFrame(data, columns=columns)
pd.set_option('display.max_rows', None)  # แสดงแถวทั้งหมด
pd.set_option('display.max_columns', None)  # แสดงคอลัมน์ทั้งหมด
pd.set_option('display.width', None)  # ปรับความกว้างให้เต็มหน้าจอ
pd.set_option('display.max_colwidth', None)  # แสดงข้อความเต็มในคอลัมน์
print(df)



# แสดงข้อมูลที่ดึงมา
print(df)

# สร้างกราฟ
labels = df['THProvince']
male_counts = df['M']
female_counts = df['F']

# ความกว้างของกราฟแท่ง
bar_width = 0.35

# กำหนดตำแหน่งสำหรับกราฟแท่ง
index = range(len(labels))

# สร้างกราฟแท่ง
fig, ax = plt.subplots(figsize=(10, 6))

bar1 = ax.bar(index, male_counts, bar_width, label='ผู้ชาย', color='blue')
bar2 = ax.bar([p + bar_width for p in index], female_counts, bar_width, label='ผู้หญิง', color='pink')

# เพิ่มข้อมูลที่แสดงบนแท่ง
ax.bar_label(bar1)
ax.bar_label(bar2)

# ตั้งชื่อกราฟและแกน
ax.set_xlabel('กลุ่ม')
ax.set_ylabel('จำนวน')
ax.set_title('การเปรียบเทียบจำนวนผู้ชายและผู้หญิงในแต่ละกลุ่ม')

# ตั้งค่าตำแหน่งของ label บนแกน X
ax.set_xticks([p + bar_width / 2 for p in index])
ax.set_xticklabels(labels)

# เพิ่มกริด, ตาราง และคำอธิบาย
ax.legend()
ax.grid(True)

# แสดงกราฟ
plt.tight_layout()
plt.show()

