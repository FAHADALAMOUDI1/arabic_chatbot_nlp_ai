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
