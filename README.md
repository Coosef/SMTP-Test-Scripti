# 📧 SMTP Test Scripti

Bu Python scripti, bir SMTP sunucusuna bağlanarak test e-postası gönderir. TLS üzerinden oturum açma, e-posta gönderme ve hata kontrolü işlemlerini kapsar.

## 🚀 Özellikler

- TLS ile güvenli bağlantı kurar
- SMTP oturum açma (authentication) desteği
- Belirlenen adrese test e-postası gönderir
- Hataları kullanıcı dostu şekilde gösterir
- E-posta adresi doğrulama kontrolü içerir

## 🛠️ Gereksinimler

- Python 3.6 veya üzeri
- SMTP bilgileri (sunucu, kullanıcı adı, şifre)

## 📦 Kurulum

1. Bu repo'yu klonlayın:

```bash
git clone https://github.com/Coosef/smtp-tester.git
cd smtp-tester
```

2. Gerekli kütüphaneleri yükleyin (Python’un standart modülleridir, ek kurulum gerekmez).

3. `smtp_test.py` dosyasını açın ve SMTP bilgilerinizi girin:

```python
smtp_server = "smtp.office365.com"
smtp_port = 587
smtp_user = "scanner@atghotels.com"
smtp_password = "SIFRENIZ"
receiver_email = "emre.basmaci@atghotels.com"
```

## ▶️ Kullanım

Terminal veya VS Code üzerinden çalıştırabilirsiniz:

```bash
python smtp_test.py
```

Örnek çıktı:

```
📡 Sunucuya bağlanılıyor...
🔐 TLS bağlantısı kuruldu.
🔑 SMTP sunucusuna giriş yapılıyor...
✅ Giriş başarılı!
✉️ Mail gönderiliyor → emre.basmaci@atghotels.com
📬 Mail başarıyla gönderildi!
```

## ⚠️ Olası Hatalar ve Açıklamaları

| Hata Mesajı                     | Açıklama                                                                 |
|----------------------------------|--------------------------------------------------------------------------|
| `SMTPAuthenticationError`        | Kullanıcı adı veya şifre yanlış.                                         |
| `SMTPConnectError`               | SMTP sunucusuna bağlantı kurulamadı.                                     |
| `554 Mailbox Full`              | Alıcı e-posta kutusu dolu, teslim edilemedi.                             |
| `Invalid email address format`  | Yazım hatası yapılmış e-posta adresi.                                    |

## 🔒 Güvenlik Uyarısı

Bu script örnek amaçlıdır. Gerçek projelerde şifrelerinizi `.env` dosyasında tutun ve `dotenv` gibi kütüphaneler kullanarak okuyun.

## 🧪 Geliştirilecek Özellikler (Opsiyonel)

- GUI destekli test paneli (PyQt5 veya Tkinter ile)
- Toplu e-posta gönderimi
- Loglama (log dosyasına kayıt)
- SMTP sunucu izleme (monitoring)

## 📄 Lisans

MIT License. Serbestçe kullanılabilir.

---

Hazırlayan: **[Coosef](https://github.com/kullaniciadi)**
