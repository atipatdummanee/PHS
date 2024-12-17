
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ตั้งค่าฟอนต์สำหรับภาษาไทย
plt.rcParams['font.family']='tahoma'

# การเชื่อมต่อ MySQL
username = 'root'
password = 'rootpassword'
host = 'localhost'
database = 'mydb'
connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
engine = create_engine(connection_string)

# SQL Query
query = '''
SELECT
    MONTH(Service_Date) AS month, 
    COUNT(CASE WHEN TitleName IN ('นาย ','หญิง','นายแพทย์','แพทย์หญิง','นางสาว','ว่าที่ร้อยตรีหญิง')THEN 1  END) AS layperson,  
    COUNT(CASE WHEN TitleName IN ('พระภิกษุ ','พระมหา','พระปลัด','พระครูสมุห์','พระอธิการ','พระครูใบฎีกา','พระครูสังฆรักษ์','พระครูวนัยธร','สามเณร')THEN 1  END) AS Monk 
FROM clinicvisit
WHERE Service_Date BETWEEN '2020-01-01' AND '2024-12-31'
GROUP BY month
ORDER BY month
'''

# ดึงข้อมูลจาก MySQL
df = pd.read_sql(query, engine)

# ปิดการเชื่อมต่อ
engine.dispose()

# ตรวจสอบข้อมูลที่ดึงมา
print(df)

# สร้างลิสต์ของชื่อเดือนในภาษาไทย
thai_months = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

# แปลงเดือนจากตัวเลขเป็นชื่อเดือนในภาษาไทย
df['month_th'] = df['month'].apply(lambda x: thai_months[x - 1])

# สร้างกราฟวงกลม
labels = df['month_th']  # ชื่อเดือนในภาษาไทย
layperson_counts = df['layperson']  # จำนวนฆารวาส
monk_counts = df['Monk']  # จำนวนพระ

# รวมจำนวนฆารวาสและพระ
total_counts = layperson_counts + monk_counts

# สร้างกราฟวงกลมแยกฆารวาสและพระ
fig, ax = plt.subplots(figsize=(8, 8))  # ขนาดของกราฟ

# ใช้ autopct ในการแสดงเป็นจำนวนเต็ม
ax.pie(total_counts, labels=labels, autopct=lambda p: f'{int(p * sum(total_counts) / 100)}', startangle=90, colors=['blue', 'pink'], textprops={'fontsize': 12, 'fontfamily': 'tahoma'})

# ชื่อกราฟ
ax.set_title('การเปรียบเทียบจำนวนฆารวาสและพระในแต่ละเดือน')

# แสดงกราฟ
plt.tight_layout()
plt.show()