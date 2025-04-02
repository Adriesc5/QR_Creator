import qrcode
from PIL import Image, ImageDraw, ImageFont
import os


def generar_qr_con_logo(data: str, logo_path: str, texto_value: str, base_output_dir: str, texto_descriptivo: str = ""):
    qr_color = "#112D4E"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=20,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color=qr_color, back_color="white").convert('RGBA')

    logo = Image.open(logo_path).convert("RGBA")
    qr_width, qr_height = img_qr.size
    logo_size = int(qr_width * 0.18)
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    texto_label = "Asset: "
    try:
        fuente_negrita = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size=42)
        fuente_normal = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=42)
        fuente_descriptivo = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size=42)
    except OSError:
        fuente_negrita = ImageFont.load_default()
        fuente_normal = ImageFont.load_default()
        fuente_descriptivo = ImageFont.load_default()

    draw_temp = ImageDraw.Draw(img_qr)
    label_bbox = draw_temp.textbbox((0, 0), texto_label, font=fuente_negrita)
    value_bbox = draw_temp.textbbox((0, 0), texto_value, font=fuente_normal)
    desc_bbox = draw_temp.textbbox((0, 0), texto_descriptivo, font=fuente_descriptivo)

    texto_ancho = label_bbox[2] - label_bbox[0] + value_bbox[2] - value_bbox[0]
    texto_alto = max(label_bbox[3] - label_bbox[1], value_bbox[3] - value_bbox[1])
    desc_ancho = desc_bbox[2] - desc_bbox[0]
    desc_alto = desc_bbox[3] - desc_bbox[1] if texto_descriptivo else 0

    padding_logo_top = 5
    padding_text_between = 20  # Aumentado el espaciado entre líneas
    content_width = max(texto_ancho, desc_ancho)
    text_block_height = texto_alto + padding_text_between + desc_alto
    header_height = max(logo_size + 2 * padding_logo_top, text_block_height + 2 * padding_logo_top)
    canvas_height = header_height + qr_height

    canvas = Image.new("RGBA", (qr_width, canvas_height), "white")
    draw = ImageDraw.Draw(canvas)

    logo_x = padding_logo_top
    logo_y = (header_height - logo_size) // 2
    canvas.paste(logo, (logo_x, logo_y), mask=logo)

    text_area_x = logo_x + logo_size + 15
    text_area_width = qr_width - text_area_x - padding_logo_top

    text_x = text_area_x + (text_area_width - texto_ancho) // 2
    asset_y = (header_height - text_block_height) // 2
    desc_y = asset_y + texto_alto + padding_text_between

    draw.text((text_x, asset_y), texto_label, fill=qr_color, font=fuente_negrita)
    draw.text((text_x + (label_bbox[2] - label_bbox[0]), asset_y), texto_value, fill=qr_color, font=fuente_normal)

    if texto_descriptivo:
        draw.text((text_area_x + (text_area_width - desc_ancho) // 2, desc_y), texto_descriptivo, fill=qr_color, font=fuente_descriptivo)

    canvas.paste(img_qr, (0, header_height))
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
    output_dir = "output_qrs_Name"
    asset_file = "assetsName.txt"

    asset_list = leer_assets_desde_txt(asset_file)

    for asset in asset_list:
        parts = asset.split(' - ')
        texto_value = parts[0]
        texto_descriptivo = parts[1] if len(parts) > 1 else ""
        generar_qr_con_logo(data_base_url, logo_path, texto_value, output_dir, texto_descriptivo)
