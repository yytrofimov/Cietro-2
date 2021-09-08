from __init__ import *


def make_qr(activation_code: str):
    img = qrcode.make(activation_code)
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        return output.getvalue()
