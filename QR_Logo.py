import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


def generar_qr_con_logo(data: str, logo_path: str, texto_value: str, base_output_dir: str):
    qr_color = "#112D4E"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color=qr_color, back_color="white").convert('RGBA')

    logo = Image.open(logo_path).convert("RGBA")
    qr_width, qr_height = img_qr.size
    logo_size = int(qr_width * 0.22)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    texto_label = "Asset:"
    try:
        fuente_negrita = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size=34)
        fuente_normal = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=33)
    except OSError:
        fuente_negrita = ImageFont.load_default()
        fuente_normal = ImageFont.load_default()

    draw_temp = ImageDraw.Draw(img_qr)
    label_bbox = draw_temp.textbbox((0, 0), texto_label, font=fuente_negrita)
    value_bbox = draw_temp.textbbox((0, 0), texto_value, font=fuente_normal)
    texto_ancho = (label_bbox[2] - label_bbox[0]) + (value_bbox[2] - value_bbox[0])
    texto_alto = max(label_bbox[3] - label_bbox[1], value_bbox[3] - value_bbox[1])

    header_height = max(logo_size, texto_alto)
    header_width = qr_width

    canvas = Image.new("RGBA", (header_width, header_height + qr_height), "white")
    canvas.paste(img_qr, (0, header_height))
    logo_x = 0
    logo_y = (header_height - logo_size) // 2
    canvas.paste(logo, (logo_x, logo_y), mask=logo)

    draw = ImageDraw.Draw(canvas)
    texto_x = logo_size + 10
    texto_y = (header_height - texto_alto) // 2
    draw.text((texto_x, texto_y), texto_label, fill=qr_color, font=fuente_negrita)
    draw.text((texto_x + (label_bbox[2] - label_bbox[0]), texto_y), texto_value, fill=qr_color, font=fuente_normal)

    canvas = canvas.convert('RGB')
    prefix_folder = texto_value.strip().split('-')[0]
    output_dir = os.path.join(base_output_dir, prefix_folder)
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{texto_value.strip()}.jpg"
    output_path = os.path.join(output_dir, filename)
    canvas.save(output_path)

def leer_assets_desde_txt(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    data_base_url = "https://vtc.managerpluscloud.com/lt/portals/GTCCorp/main/open"
    logo_path = "TMCDL-oNLY WORLD.png"
    output_dir = "output_qrs"
    asset_file = "assets.txt"  # <- nombre del archivo .txt con un asset por línea

    asset_list = leer_assets_desde_txt(asset_file)

    for asset in asset_list:
        generar_qr_con_logo(data_base_url, logo_path, asset, output_dir)
