# 🌍 IP Address Tracker - Web App

**Real-time IP Address Tracking va Geolokatsiya Web Platformasi**

IP addresslarni qidiring, lokatsiyalarini aniqlang va xaritada ko'ring!

## ✨ Xususiyatlar

✅ **IP Address Qidirish** - Har qanday IP-ni aniqlash  
✅ **Geolokatsiya Xaritalari** - Leaflet bilan interaktiv xaritalar  
✅ **Detalliy Ma'lumotlar** - Country, City, ISP, Timezone, ASN va boshqalar  
✅ **Real-time Lokatsiya** - Latitude va Longitude  
✅ **VPN/Proxy Aniqlash** - Security features  
✅ **Lookup Tarixi** - Oxirgi qidiruvlarni saqlash  
✅ **Batch Lookup** - Ko'p IP addresslarni qidirish  
✅ **O'z IP-ni Aniqlash** - "O'z IP-m" tugmasi  
✅ **Beautiful UI** - Modern gradient dizayn  
✅ **Mobile Responsive** - Barcha qurilmalarda ishlash  

## 🚀 Ishlatish

### 1. Repository-ni clone qiling:
```bash
git clone https://github.com/alibekde/ip-address-tracker.git
cd ip-address-tracker
```

### 2. Virtual environment yaratish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows
```

### 3. Kerakli kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 4. Dasturni ishga tushiring:
```bash
python app.py
```

### 5. Brauzeringizda oching:
```
http://localhost:5000
```

---

## 📖 Qanday Ishlash

### 1️⃣ **IP Address Kiriting**
- "IP address kiriting" maydoniga IP yozing
- Masalan: `8.8.8.8`, `1.1.1.1`, `208.67.222.222`

### 2️⃣ **Qidirish**
- 🔍 "Qidirish" tugmasini bosing
- Yoki Enter-ni bosing

### 3️⃣ **Ma'lumotlarni Ko'rish**
- IP address
- Mamlakat va Shahar
- ISP/Organizatsiya
- Vaqt mintaqasi
- VPN/Proxy status

### 4️⃣ **Xaritada Ko'rish**
- Lokatsiya xaritada ko'rinadi
- Marker bilan aniqlanadi
- Zoom qilish mumkin

### 5️⃣ **O'z IP-ni Aniqlash**
- 📱 "O'z IP-m" tugmasini bosing
- Kompyuteringizning IP-i ko'rinadi

---

## 🔗 API Endpoints

### IP Qidirish
```bash
POST /api/lookup
Body: {"ip": "8.8.8.8"}
```

### O'z IP-ni Olish
```bash
GET /api/my-ip
```

### Batch Lookup
```bash
POST /api/batch-lookup
Body: {"ips": ["8.8.8.8", "1.1.1.1", "208.67.222.222"]}
```

### IP Validatsiyasi
```bash
POST /api/validate-ip
Body: {"ip": "192.168.1.1"}
```

### Lookup Tarixi
```bash
GET /api/history
```

---

## 📊 Qabul Qiladigan Ma'lumotlar

| Ma'lumot | Tavsifi |
|----------|--------|
| **IP Address** | Public va Private IP |
| **Country** | Mamlakat nomi |
| **City** | Shahar nomi |
| **Region** | Viloyat/Region |
| **Timezone** | UTC offset |
| **ISP** | Internet Service Provider |
| **ASN** | Autonomous System Number |
| **Latitude** | Kuzey/Janub koordinatasi |
| **Longitude** | Sharq/Gʻarb koordinatasi |
| **Postal Code** | Pochta indeksi |
| **Currency** | Valyuta |
| **Languages** | Qo'llaniladigan tillar |
| **VPN** | VPN ekanligini tekshirish |
| **Proxy** | Proxy ekanligini tekshirish |
| **Datacenter** | Datacenter IP ekanligini tekshirish |

---

## 📝 Misol IP Addresslar

**Public DNS-lar:**
- `8.8.8.8` - Google DNS
- `1.1.1.1` - Cloudflare DNS
- `208.67.222.222` - OpenDNS

**Corporate:**
- `13.107.42.14` - Microsoft
- `31.13.64.35` - Meta (Facebook)
- `151.101.65.140` - Fastly

---

## 🛡️ Xavfsizlik

✅ IP Validation  
✅ Private IP tekshirish  
✅ XSS himoyasi  
✅ Rate limiting (optional)  
✅ Error handling  

---

## 🌐 Deployment

### Render.com-da Deploy

1. Repository-ni GitHub-ga push qiling
2. Render.com-ga kiring
3. "New Web Service" yarating
4. GitHub repository-ni ulang
5. **Build Command:**
   ```
   pip install -r requirements.txt
   ```
6. **Start Command:**
   ```
   gunicorn app:app
   ```
7. Deploy bosing!

---

## 📦 Talablar

- Python 3.7+
- Flask 3.0+
- Requests 2.31+
- Gunicorn (production)

---

## 🗺️ Map Library

**Leaflet.js** - Open-source xarita library
- Lightweight va tezkor
- OpenStreetMap tiles
- Responsive design

---

## 🎯 Features Deep Dive

### IP Qidirish
- Public va Private IP qo'llabi
- Real-time ma'lumotlar
- ipapi.co API-dan foydalanish

### Geolokatsiya
- Latitude/Longitude
- Leaflet xaritalari
- Marker va Popup

### Security
- VPN aniqlash
- Proxy aniqlash
- Datacenter aniqlash

### History
- Oxirgi 10 ta qidiruv
- Click-ga qayta qidiruv
- Timestamp va lokatsiya

---

## 🚨 Troubleshooting

### "Xarita ko'rinmaydi"
```bash
# Check browser console (F12)
# Leaflet CDN yuklandi?
```

### "IP topilmadi"
- Private IP ni tekshirib ko'ring (192.168.x.x, 10.x.x.x)
- API rate limiting?
- Internet ulanmagan?

### "LocationError"
- ipapi.co API sozlamalari
- CORS setting

---

## 📄 Litsenziya

MIT License

---

## 👨‍💻 Muallif

[@alibekde](https://github.com/alibekde)

---

**IP addresslarni qidiring, dunyoni kuzating!** 🌍📍
