import mysql.connector
import pandas as pd



# ตั้งค่าฟอนต์สำหรับภาษาไทย
#plt.rcParams['font.family']='tahoma'

# การเชื่อมต่อ MySQL

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpassword",
    database="mysql-docker"
)



# แสดงข้อมูลที่ดึงมา
print(df)

# สร้างกราฟ
labels = df['THProvince']
male_counts = df['male']
female_counts = df['female']

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