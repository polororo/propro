import qrcode

# Secret OTP pour Google Authenticator
otp_secret = "secretotp du compte"

# URL au format pour Google Authenticator
uri = f"otpauth://totp/Google:{otp_secret}?secret={otp_secret}&issuer=Google"

# Générer le QR code
qr = qrcode.make(uri)

# Afficher le QR code
qr.show()