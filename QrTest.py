import qrcode
from PIL import Image

# Datos que se incluirán en el código QR
data = "https://vtc.managerpluscloud.com/lt/portals/GTCCorp/main/open"

# Crear el objeto QRCode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Agregar los datos al QR
qr.add_data(data)
qr.make(fit=True)

# Generar la imagen del código QR
img = qr.make_image(fill_color="black", back_color="white")

# Guardar la imagen en un archivo PNG
img.save("qr_code.png")

# (Opcional) Mostrar la imagen
img.show()
