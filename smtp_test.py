import smtplib
import ssl
import re
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ============================================================
# SMTP AYARLARI
# ============================================================

smtp_server = "SMTP_SERVER"
smtp_port = 587

smtp_user = "Sender_Email"
smtp_password = "Sender_Email_Password"


# ============================================================
# GÖNDERİCİ / ALICI
# ============================================================

sender_email = smtp_user
receiver_email = "Receiver_Email_Addres"


# ============================================================
# E-POSTA İÇERİĞİ
# ============================================================

subject = "SMTP Test Maili"

body = """Merhaba,

Bu bir SMTP test mailidir.

Eğer bu mesajı alıyorsanız, SMTP yapılandırmanız başarıyla çalışıyor demektir.

İyi çalışmalar!
"""


# ============================================================
# GENEL AYARLAR
# ============================================================

SMTP_TIMEOUT = 20

# True yaparsan Python SMTP protokol trafiğini terminale yazdırır.
# DİKKAT:
# Debug çıktısında AUTH bilgileri/base64 veriler görülebileceği için
# bu çıktıyı başkalarıyla paylaşma.
SMTP_DEBUG = False


# ============================================================
# E-POSTA ADRESİ KONTROLÜ
# ============================================================

def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


# ============================================================
# SMTP HATA MESAJINI GÜVENLİ ŞEKİLDE DECODE ET
# ============================================================

def decode_smtp_error(error):
    if isinstance(error, bytes):
        return error.decode("utf-8", errors="replace")

    return str(error)


# ============================================================
# SMTP TESTİ
# ============================================================

def test_smtp():
    print("=" * 65)
    print("Microsoft 365 SMTP Test")
    print("=" * 65)

    print(f"SMTP Server : {smtp_server}")
    print(f"SMTP Port   : {smtp_port}")
    print(f"SMTP User   : {smtp_user}")
    print(f"Sender      : {sender_email}")
    print(f"Receiver    : {receiver_email}")
    print()

    # --------------------------------------------------------
    # E-posta adreslerini doğrula
    # --------------------------------------------------------

    if not is_valid_email(sender_email):
        print(
            f"❌ Gönderici e-posta adresi geçersiz görünüyor: "
            f"{sender_email}"
        )
        return

    if not is_valid_email(receiver_email):
        print(
            f"❌ Alıcı e-posta adresi geçersiz görünüyor: "
            f"{receiver_email}"
        )
        return

    # --------------------------------------------------------
    # MIME mesajı oluştur
    # --------------------------------------------------------

    message = MIMEMultipart()

    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "plain",
            "utf-8"
        )
    )

    # --------------------------------------------------------
    # TLS context
    # --------------------------------------------------------

    tls_context = ssl.create_default_context()

    try:
        # ----------------------------------------------------
        # TCP / SMTP bağlantısı
        # ----------------------------------------------------

        print("📡 SMTP sunucusuna bağlanılıyor...")

        with smtplib.SMTP(
            smtp_server,
            smtp_port,
            timeout=SMTP_TIMEOUT
        ) as server:

            if SMTP_DEBUG:
                server.set_debuglevel(1)

            print("✅ SMTP sunucusuna TCP bağlantısı kuruldu.")

            # ------------------------------------------------
            # İlk EHLO
            # ------------------------------------------------

            print("📨 SMTP EHLO gönderiliyor...")

            ehlo_code, ehlo_message = server.ehlo()

            print(f"✅ EHLO sonucu: {ehlo_code}")

            if ehlo_code != 250:
                print(
                    "⚠️ Sunucu EHLO isteğine beklenen 250 "
                    "cevabını vermedi."
                )

            # ------------------------------------------------
            # STARTTLS desteği
            # ------------------------------------------------

            if not server.has_extn("starttls"):
                print(
                    "❌ SMTP sunucusu STARTTLS desteği "
                    "bildirmedi."
                )
                return

            print("🔐 STARTTLS başlatılıyor...")

            tls_code, tls_message = server.starttls(
                context=tls_context
            )

            print(
                f"✅ TLS bağlantısı kuruldu. "
                f"SMTP sonucu: {tls_code}"
            )

            # ------------------------------------------------
            # TLS sonrası tekrar EHLO
            # ------------------------------------------------

            print("📨 TLS sonrası EHLO tekrar gönderiliyor...")

            ehlo_code, ehlo_message = server.ehlo()

            print(f"✅ EHLO sonucu: {ehlo_code}")

            # ------------------------------------------------
            # SMTP sunucusunun özelliklerini göster
            # ------------------------------------------------

            print()
            print("🔎 SMTP sunucusunun bildirdiği özellikler:")

            for feature, value in server.esmtp_features.items():
                if feature.lower() == "auth":
                    print(
                        f"   AUTH mekanizmaları : {value}"
                    )
                else:
                    print(
                        f"   {feature.upper():18}: {value}"
                    )

            print()

            # ------------------------------------------------
            # AUTH desteğini kontrol et
            # ------------------------------------------------

            if not server.has_extn("auth"):
                print(
                    "❌ SMTP sunucusu AUTH desteği "
                    "bildirmedi."
                )
                return

            auth_methods = server.esmtp_features.get(
                "auth",
                "Bilinmiyor"
            )

            print(
                f"🔑 SMTP AUTH mekanizmaları: "
                f"{auth_methods}"
            )

            # ------------------------------------------------
            # LOGIN
            # ------------------------------------------------

            print()
            print("🔑 Microsoft 365 SMTP AUTH deneniyor...")

            try:
                server.login(
                    smtp_user,
                    smtp_password
                )

            except smtplib.SMTPAuthenticationError as auth_error:

                error_message = decode_smtp_error(
                    auth_error.smtp_error
                )

                print()
                print("=" * 65)
                print("❌ SMTP AUTHENTICATION BAŞARISIZ")
                print("=" * 65)

                print(
                    f"SMTP Kod     : "
                    f"{auth_error.smtp_code}"
                )

                print(
                    f"SMTP Mesajı  : "
                    f"{error_message}"
                )

                print()

                if auth_error.smtp_code == 535:

                    print(
                        "Microsoft 365 kullanıcı adı/parola "
                        "authentication isteğini reddetti."
                    )

                    print()
                    print(
                        "Bu sonuç TLS veya network problemi "
                        "olmadığını gösterir."
                    )

                    print()
                    print(
                        "Kontrol edilmesi gereken başlıca "
                        "alanlar:"
                    )

                    print(
                        "  1. Kullanıcı adı / parola"
                    )

                    print(
                        "  2. SMTP AUTH mailbox ayarı"
                    )

                    print(
                        "  3. Tenant SMTP AUTH ayarı"
                    )

                    print(
                        "  4. Security Defaults"
                    )

                    print(
                        "  5. Conditional Access"
                    )

                    print(
                        "  6. Legacy / Basic Authentication "
                        "politikaları"
                    )

                    print(
                        "  7. MFA / authentication yöntemi"
                    )

                    print(
                        "  8. Entra ID Sign-in Logs"
                    )

                return

            print("✅ SMTP authentication başarılı!")

            # ------------------------------------------------
            # Mail gönder
            # ------------------------------------------------

            print()
            print(
                f"✉️ Mail gönderiliyor → "
                f"{receiver_email}"
            )

            refused_recipients = server.sendmail(
                sender_email,
                [receiver_email],
                message.as_string()
            )

            if refused_recipients:
                print(
                    "⚠️ SMTP sunucusu bazı alıcıları "
                    "reddetti:"
                )

                for recipient, error in refused_recipients.items():
                    print(
                        f"   {recipient}: {error}"
                    )

                return

            print("📬 Mail başarıyla gönderildi!")

            print()
            print("=" * 65)
            print("✅ SMTP TESTİ BAŞARILI")
            print("=" * 65)

    # ========================================================
    # SMTP CONNECT ERROR
    # ========================================================

    except smtplib.SMTPConnectError as e:

        print()
        print("❌ SMTP sunucusuna bağlanılamadı.")

        print(
            f"SMTP Kod    : {e.smtp_code}"
        )

        print(
            f"SMTP Mesajı : "
            f"{decode_smtp_error(e.smtp_error)}"
        )

    # ========================================================
    # SMTP RECIPIENT REFUSED
    # ========================================================

    except smtplib.SMTPRecipientsRefused as e:

        print()
        print("❌ SMTP sunucusu alıcı adresini reddetti.")

        for recipient, error in e.recipients.items():
            print(
                f"{recipient}: {error}"
            )

    # ========================================================
    # SMTP SENDER REFUSED
    # ========================================================

    except smtplib.SMTPSenderRefused as e:

        print()
        print("❌ SMTP sunucusu gönderici adresini reddetti.")

        print(
            f"SMTP Kod    : {e.smtp_code}"
        )

        print(
            f"SMTP Mesajı : "
            f"{decode_smtp_error(e.smtp_error)}"
        )

        print(
            f"Gönderici   : {e.sender}"
        )

    # ========================================================
    # SMTP DATA ERROR
    # ========================================================

    except smtplib.SMTPDataError as e:

        print()
        print(
            "❌ SMTP sunucusu mesaj içeriğini "
            "kabul etmedi."
        )

        print(
            f"SMTP Kod    : {e.smtp_code}"
        )

        print(
            f"SMTP Mesajı : "
            f"{decode_smtp_error(e.smtp_error)}"
        )

    # ========================================================
    # DİĞER SMTP HATALARI
    # ========================================================

    except smtplib.SMTPResponseException as e:

        print()
        print("❌ SMTP sunucusu hata döndürdü.")

        print(
            f"SMTP Kod    : {e.smtp_code}"
        )

        print(
            f"SMTP Mesajı : "
            f"{decode_smtp_error(e.smtp_error)}"
        )

    # ========================================================
    # DNS HATASI
    # ========================================================

    except socket.gaierror as e:

        print()
        print("❌ SMTP sunucusunun DNS çözümlemesi başarısız.")

        print(
            f"Hata: {e}"
        )

    # ========================================================
    # TIMEOUT
    # ========================================================

    except (socket.timeout, TimeoutError):

        print()
        print(
            f"❌ SMTP bağlantısı {SMTP_TIMEOUT} saniye "
            "içinde tamamlanamadı."
        )

    # ========================================================
    # TLS / SSL HATASI
    # ========================================================

    except ssl.SSLError as e:

        print()
        print("❌ TLS/SSL bağlantı hatası.")

        print(
            f"Hata: {e}"
        )

    # ========================================================
    # GENEL HATA
    # ========================================================

    except Exception as e:

        print()
        print("⚠️ Beklenmeyen bir hata oluştu.")

        print(
            f"Hata Türü : {type(e).__name__}"
        )

        print(
            f"Hata      : {e}"
        )


# ============================================================
# PROGRAM BAŞLANGICI
# ============================================================

if __name__ == "__main__":
    test_smtp()
