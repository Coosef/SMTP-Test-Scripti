import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === SMTP Ayarları ===
smtp_server = "smtp Server"
smtp_port = 587  # TLS için port
smtp_user = "gönderecek mail"
smtp_password = "Password"

# === Gönderici / Alıcı ===
sender_email = smtp_user
receiver_email = "Alıcı mail"  # LÜTFEN BURADA .comm değil .com olduğuna dikkat et

# === E-posta içeriği ===
subject = "SMTP Test Maili"
body = "Merhaba,\n\nBu bir SMTP test mailidir. Eğer bu mesajı alıyorsanız, SMTP yapılandırmanız başarıyla çalışıyor demektir.\n\nİyi çalışmalar!"

# === E-posta adresi kontrol fonksiyonu ===
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# === Başlat ===
if not is_valid_email(receiver_email):
    print(f"❗ Uyarı: Alıcı e-posta adresi geçersiz görünüyor → {receiver_email}")
else:
    # MIME oluştur
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # SMTP işlemi
    try:
        print("📡 Sunucuya bağlanılıyor...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("🔐 TLS bağlantısı kuruldu.")

        print("🔑 SMTP sunucusuna giriş yapılıyor...")
        server.login(smtp_user, smtp_password)
        print("✅ Giriş başarılı!")

        print(f"✉️ Mail gönderiliyor → {receiver_email}")
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("📬 Mail başarıyla gönderildi!")

        server.quit()

    except smtplib.SMTPResponseException as e:
        print(f"❌ SMTP sunucusu hata verdi ({e.smtp_code}): {e.smtp_error.decode()}")
    except smtplib.SMTPAuthenticationError:
        print("❌ Giriş başarısız! Kullanıcı adı veya şifre yanlış olabilir.")
    except smtplib.SMTPConnectError:
        print("❌ SMTP sunucusuna bağlanılamadı. İnternet bağlantınızı veya sunucu adresini kontrol edin.")
    except Exception as e:
        print(f"⚠️ Beklenmeyen bir hata oluştu: {e}")
