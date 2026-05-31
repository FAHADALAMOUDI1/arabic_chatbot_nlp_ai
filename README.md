# 🤖 NLE AI Arabic Chatbot

## مساعد الذكاء الاصطناعي العربي المتقدم

مشروع شات بوت عربي احترافي يفهم اللغة العربية ويدعم API RESTful مع واجهة تفاعلية حديثة.

## ✨ المميزات

- 🗣️ **فهم اللغة العربية العميق** - معالجة NLP متقدمة للنصوص العربية
- 🎯 **تعرف النوايا (Intent Recognition)** - تحديد دقيق لنية المستخدم
- 💾 **السياق** - حفظ سياق المحادثة لكل مستخدم
- 🔌 **API RESTful** - واجهة برمجة سهلة الدمج
- 📱 **تصميم متجاوب** - يعمل على جميع الأجهزة
- ⚡ **أداء عالي** - استجابة سريعة وفعالة

## 🚀 التشغيل

### 1. تثبيت المتطلبات

```bash
pip install -r requirements.txt
```

### 2. تشغيل التطبيق

```bash
python app.py
```

### 3. فتح المتصفح

افتح: `http://localhost:5000`

## 📡 API Endpoints

| Method | Endpoint | الوصف |
|--------|----------|-------|
| POST | `/api/chat` | إرسال رسالة والحصول على رد |
| GET | `/api/health` | فحص حالة النظام |
| GET | `/api/history` | تاريخ المحادثات |
| GET | `/api/stats` | إحصائيات النظام |

### مثال على استخدام API

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "مرحبا", "user_id": "user_123"}'
```

## 🏗️ هيكل المشروع

```
arabic_chatbot/
├── app.py              # Flask Backend
├── requirements.txt    # المتطلبات
├── README.md          # التوثيق
├── static/
│   ├── css/
│   │   └── style.css   # التصميم
│   └── js/
│       └── app.js      # التفاعل
└── templates/
    └── index.html      # الواجهة
```

## 🛠️ التقنيات

- **Python 3.8+**
- **Flask** - إطار العمل
- **JavaScript (Vanilla)** - الواجهة الأمامية
- **CSS3** - التصميم المتجاوب
- **Regex NLP** - معالجة اللغة العربية

## 👨‍💻 المطور

تم التطوير بواسطة فريق **ENG.FAHAD ALAMOUDI**

## 📄 الرخصة

MIT License



<img width="2544" height="1298" alt="3333" src="https://github.com/user-attachments/assets/e16b3031-4474-438f-bdb5-167b2bcb6de0" />

<img width="2533" height="1296" alt="4444" src="https://github.com/user-attachments/assets/2645ce19-f3b4-4bc1-af5a-691eae0914ca" />

<img width="2544" height="1308" alt="5555" src="https://github.com/user-attachments/assets/5c05b174-4b6a-4ab6-b8c5-b4d55dd3c7b7" />

<img width="2544" height="1295" alt="6666" src="https://github.com/user-attachments/assets/404601e3-d837-418f-b7db-5ecba603c93c" />





