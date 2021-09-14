import qrcode
import io


def make_qr(data: str):
    img = qrcode.make(data)
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        return output.getvalue()
