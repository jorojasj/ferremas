import base64

PAYPAL_CLIENT_ID = 'AVT-jXZsVPASeIqoIzFvCH4ApgAZAzrCd9jYwJy1Dc2yyuuBRmqApMmJCvdY02x9CZS3dPhupARiJ-tk'
PAYPAL_CLIENT_SECRET = 'AVT-jXZsVPASeIqoIzFvCH4ApgAZAzrCd9jYwJy1Dc2yyuuBRmqApMmJCvdY02x9CZS3dPhupARiJ-tk'
BASE_URL = "https://api-m.sandbox.paypal.com"

def generateAccessToken():
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError('No hay credenciales')
    
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode("utf-8")