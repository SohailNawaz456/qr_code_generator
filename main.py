import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

# Streamlit App Title
st.title("📌 QR Code Generator")
st.write("Generate a customized QR code with your own text and color! ✅")

# User Input
data = st.text_input("Enter your URL or text:", "https://www.google.com")
qr_color = st.color_picker("Pick a QR Code Color", "#008000")  # Default Green
bg_color = st.color_picker("Pick Background Color", "#FFFFFF")  # Default White
custom_text = st.text_input("Enter text below QR Code:", "✅ Created by Sohail Nawaz 🚀")

# Button to Generate QR Code
if st.button("Generate QR Code"):
    # Create QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate QR Image
    qr_img = qr.make_image(fill_color=qr_color, back_color=bg_color).convert("RGB")

    # Add Custom Text Below QR Code
    font_size = 20
    text_img = Image.new('RGB', (qr_img.width, qr_img.height + 50), bg_color)
    draw = ImageDraw.Draw(text_img)

    # Load Font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Calculate Text Position
    bbox = draw.textbbox((0, 0), custom_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (qr_img.width - text_width) // 2
    text_y = qr_img.height + 10

    # Paste QR Code on New Image
    text_img.paste(qr_img, (0, 0))

    # Draw Custom Text
    draw.text((text_x, text_y), custom_text, fill="black", font=font)

    # Convert Image to Bytes
    img_bytes = io.BytesIO()
    text_img.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    # Display QR Code with Updated `use_container_width`
    st.image(text_img, caption="Your Custom QR Code", use_container_width=True)

    # Download Button
    st.download_button(
        label="📥 Download QR Code",
        data=img_bytes,
        file_name="custom_qrcode.png",
        mime="image/png"
    )
