import streamlit as st
import qrcode
from PIL import Image
import re
import os
from io import BytesIO

# Function to create QR code and return image bytes
def create_qr_code(link, scaling_factor=10):
    # Dynamically select QR code version based on input length
    link_length = len(link)
    
    if link_length <= 44:
        version = 2
    elif link_length <= 77:
        version = 3
    else:
        version = 4
    
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=scaling_factor,
        border=4,
    )
    
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white').convert('RGB')

    # Save to BytesIO object as JPEG
    buf = BytesIO()
    img.save(buf, format='JPEG')
    byte_im = buf.getvalue()

    return byte_im

# Streamlit App Layout
st.set_page_config(page_title="📱 QR Code Generator", page_icon="📱")

st.title("📱 QR Code Generator")

st.markdown("""
Enter a URL below to generate its corresponding QR code. You can also download the generated QR code as a JPEG image.
""")

# Input for URL
link = st.text_input("Enter the URL to generate QR Code:")

# Input for scaling factor with default value
scaling_factor = st.number_input("Enter the scaling factor (default 10):", min_value=1, max_value=20, value=10, step=1)

# Generate QR Code Button
if st.button("Generate QR Code"):
    if link:
        try:
            qr_image = create_qr_code(link, scaling_factor)

            # Display the QR code
            st.image(qr_image, caption='Your QR Code', use_column_width=True)

            # Provide download button
            st.download_button(
                label="Download QR Code as JPG",
                data=qr_image,
                file_name="qr_code.jpg",
                mime="image/jpeg",
            )
        except Exception as e:
            st.error(f"An error occurred while generating the QR code: {e}")
    else:
        st.warning("Please enter a valid URL.")
