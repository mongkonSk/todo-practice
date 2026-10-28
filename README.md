# todo-practice
claude code practice

แอป todo list แบบ command line เขียนด้วย Python เก็บข้อมูลไว้ในไฟล์ `todo.json`

## ความต้องการ

- Python 3.8 ขึ้นไป (ไม่ต้องติดตั้งไลบรารีเพิ่มสำหรับตัวแอป)
- `pytest` สำหรับรันเทสต์

## วิธีใช้

```bash
# เพิ่มรายการ
python todo.py add ซื้อนม
python todo.py add "เขียนรายงาน"

# แสดงรายการทั้งหมด
python todo.py list
# 1. ซื้อนม
# 2. เขียนรายงาน

# ลบรายการตาม id
python todo.py remove 1
```

ค่าเริ่มต้นจะเก็บข้อมูลใน `todo.json` ในโฟลเดอร์ที่รันคำสั่ง
ถ้าต้องการใช้ไฟล์อื่น ให้ใส่ `--file` ก่อนคำสั่งย่อย:

```bash
python todo.py --file mytasks.json list
```

| คำสั่ง | คำอธิบาย |
| --- | --- |
| `add <task>` | เพิ่มรายการใหม่ (id จะเพิ่มขึ้นเรื่อยๆ และไม่ถูกนำกลับมาใช้ซ้ำ) |
| `remove <id>` | ลบรายการตาม id (ถ้าไม่พบจะแสดง error และ exit code 1) |
| `list` | แสดงรายการทั้งหมด |

## รันเทสต์

```bash
pip install pytest
pytest
```
