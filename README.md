# ระบบจัดการผู้ใช้ (User Management System)

ระบบจัดการผู้ใช้ที่สร้างด้วย Flask (Backend) และ Nuxt.js (Frontend) พร้อมระบบยืนยันตัวตนด้วย JWT

## คุณสมบัติ

- ✅ ระบบลงทะเบียนผู้ใช้
- ✅ ระบบเข้าสู่ระบบ
- ✅ การตรวจสอบความถูกต้องของข้อมูล
- ✅ ระบบยืนยันตัวตนด้วย JWT
- ✅ ฐานข้อมูล MongoDB
- ✅ อินเทอร์เฟซที่ใช้งานง่าย
- ✅ การออกแบบที่สวยงามด้วยสีดำและขาว

## โครงสร้างโปรเจค

```
mini-project-eight-twelwe/
├── backend/                 # Flask Backend
│   ├── app.py              # Flask application
│   ├── config.py           # Configuration
│   ├── models.py           # Database models
│   ├── routes/             # API routes
│   │   └── auth.py         # Authentication routes
│   └── requirements.txt    # Python dependencies
├── frontend/               # Nuxt.js Frontend
│   ├── pages/              # Pages
│   │   ├── index.vue       # Home page
│   │   ├── login.vue       # Login page
│   │   └── register.vue    # Register page
│   ├── components/         # Vue components
│   ├── layouts/            # Layouts
│   ├── nuxt.config.ts      # Nuxt configuration
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## การติดตั้งและใช้งาน

### Backend (Flask)

1. เข้าไปยังโฟลเดอร์ backend:
```bash
cd backend
```

2. สร้าง virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# หรือ
venv\Scripts\activate     # Windows
```

3. ติดตั้ง dependencies:
```bash
pip install -r requirements.txt
```

4. ตั้งค่าฐานข้อมูล MongoDB ใน `config.py`

5. รันเซิร์ฟเวอร์:
```bash
python app.py
```

Backend จะทำงานที่ `http://localhost:5050`

### Frontend (Nuxt.js)

1. เข้าไปยังโฟลเดอร์ frontend:
```bash
cd frontend
```

2. ติดตั้ง dependencies:
```bash
npm install
```

3. รันเซิร์ฟเวอร์ development:
```bash
npm run dev:3030
```

Frontend จะทำงานที่ `http://localhost:3030`

## API Endpoints

### POST /api/register
ลงทะเบียนผู้ใช้ใหม่

**Request Body:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "ลงทะเบียนสำเร็จ",
  "user": {
    "id": "user_id",
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

### POST /api/login
เข้าสู่ระบบ

**Request Body:**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "message": "เข้าสู่ระบบสำเร็จ",
  "access_token": "jwt_token_here",
  "user": {
    "id": "user_id",
    "username": "testuser",
    "email": "test@example.com"
  }
}
```

## การตรวจสอบข้อมูล

### Username
- ความยาวอย่างน้อย 3 ตัวอักษร
- ต้องไม่ซ้ำกับผู้ใช้อื่น

### Email
- ต้องเป็นรูปแบบอีเมลที่ถูกต้อง
- ต้องไม่ซ้ำกับอีเมลอื่น

### Password
- ความยาวอย่างน้อย 6 ตัวอักษร

## การออกแบบ UI

- **สีหลัก**: ดำ (#000000)
- **สีรอง**: ขาว (#FFFFFF)
- **สีพื้นหลัง**: ดำและเทาเข้ม
- **สีข้อความ**: ขาวและเทาอ่อน
- **สีปุ่ม**: ขาว (พื้นหลัง) + ดำ (ข้อความ)
- **สีปุ่มรอง**: โปร่งใส + ขอบขาว + ข้อความขาว

## เทคโนโลยีที่ใช้

### Backend
- Flask - Python web framework
- Flask-JWT-Extended - JWT authentication
- Flask-CORS - Cross-origin resource sharing
- MongoEngine - MongoDB ODM
- Werkzeug - Password hashing

### Frontend
- Nuxt.js 3 - Vue.js framework
- Vue 3 - Progressive JavaScript framework
- Tailwind CSS - Utility-first CSS framework
- PostCSS - CSS processing

### Database
- MongoDB - NoSQL database

## การพัฒนาเพิ่มเติม

- [ ] เพิ่มระบบลืมรหัสผ่าน
- [ ] เพิ่มการยืนยันอีเมล
- [ ] เพิ่มระบบจัดการโปรไฟล์
- [ ] เพิ่มระบบสิทธิ์ผู้ใช้
- [ ] เพิ่มการล็อกกิจกรรม
- [ ] เพิ่มระบบแจ้งเตือน

## การแก้ไขปัญหา

### CORS Error
หากเกิด CORS error ให้ตรวจสอบว่า backend รันอยู่ที่พอร์ต 5050 และ CORS ถูกเปิดใช้งาน

### Hydration Mismatch Error
หากเกิด hydration mismatch ให้ตรวจสอบว่า:
- ใช้ `useApi()` composable สำหรับการเรียก API
- Backend และ frontend ใช้พอร์ตที่ถูกต้อง (5050 และ 3030)

### MongoDB Connection Error
ตรวจสอบการตั้งค่าฐานข้อมูลใน `config.py` และให้แน่ใจว่า MongoDB ทำงานอยู่

### Frontend Build Error
ลบโฟลเดอร์ `node_modules` และ `package-lock.json` แล้วรัน `npm install` ใหม่

### API Connection Issues
ตรวจสอบว่า:
- Backend รันที่ `http://localhost:5050`
- Frontend รันที่ `http://localhost:3030`
- ใช้ `npm run dev:3030` สำหรับ frontend

## License

<!-- MIT License -->

