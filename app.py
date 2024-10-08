import streamlit as st
import qrcode
from PIL import Image
from io import BytesIO
import qrcode.image.svg

# Function to create QR code and return image bytes or SVG string based on format
def create_qr_code(link, format='JPEG'):
    """
    Generates a QR code in the specified format.
    
    Args:
        link (str): The URL or text to encode in the QR code.
        format (str): The desired format of the QR code ('JPEG', 'PNG', 'SVG').
    
    Returns:
        tuple: A tuple containing the QR code data and its MIME type.
    """
    # Dynamically select QR code version based on input length
    link_length = len(link)
    
    if link_length <= 44:
        version = 2
    elif link_length <= 77:
        version = 3
    else:
        version = 4
    
    if format.upper() == 'SVG':
        # Use SvgImage to generate SVG format
        factory = qrcode.image.svg.SvgImage
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,  # Fixed scaling factor
            border=4,
            image_factory=factory
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image()
        
        # Convert SVG to string
        svg_data = img.to_string()
        
        # Ensure svg_data is a string, decode if it's bytes
        if isinstance(svg_data, bytes):
            svg_data = svg_data.decode('utf-8')
        
        return svg_data, 'image/svg+xml'
    
    else:
        # For PNG and JPEG formats
        qr = qrcode.QRCode(
            version=version,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,  # Fixed scaling factor
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white').convert('RGB')

        buf = BytesIO()
        img.save(buf, format=format.upper())
        byte_im = buf.getvalue()
        
        # Determine MIME type
        if format.upper() == 'PNG':
            mime_type = 'image/png'
        elif format.upper() in ['JPEG', 'JPG']:
            mime_type = 'image/jpeg'
        else:
            mime_type = 'image/png'  # Default MIME type
        
        return byte_im, mime_type

# Streamlit App Layout
st.set_page_config(page_title="📱 QR Code Generator", page_icon="📱")

st.title("📱 QR Code Generator")

st.markdown("""
Enter a URL below to generate its corresponding QR code. You can also download the generated QR code in your preferred format.
""")

# Input for URL
link = st.text_input("Enter the URL to generate QR Code:")

# Format selection
format_options = ['JPEG', 'PNG', 'SVG']
selected_format = st.selectbox("Select the format to download the QR Code:", format_options)

# Generate QR Code Button
if st.button("Generate QR Code"):
    if link:
        try:
            qr_content, mime_type = create_qr_code(link, format=selected_format)
            
            if selected_format.upper() == 'SVG':
                # Display SVG using markdown
                st.markdown(f'<div>{qr_content}</div>', unsafe_allow_html=True)
            else:
                # For PNG and JPEG, convert bytes to PIL Image and display
                image = Image.open(BytesIO(qr_content))
                st.image(image, caption='Your QR Code', use_column_width=True)
            
            # Set default file extension based on format
            if selected_format.upper() == 'JPEG':
                file_extension = 'jpg'
            elif selected_format.upper() == 'PNG':
                file_extension = 'png'
            elif selected_format.upper() == 'SVG':
                file_extension = 'svg'
            else:
                file_extension = 'png'  # Default extension
            
            # Provide download button
            st.download_button(
                label=f"Download QR Code as {selected_format}",
                data=qr_content,
                file_name=f"qr_code.{file_extension}",
                mime=mime_type,
            )
        except Exception as e:
            st.error(f"An error occurred while generating the QR code: {e}")
    else:
        st.warning("Please enter a valid URL.")
