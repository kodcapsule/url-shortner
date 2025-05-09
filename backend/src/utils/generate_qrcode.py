import qrcode


def generate_qr_code(url):
    """
    Generates a QR code for the given original URL.
    
    Args:
        url (str): The original URL to generate a QR code for
        
    Returns:
        image: the QR code image generated 
        str: The file path of the generated QR code image

    """
    try:
        # Create a QRCode object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        
        # Add data to the QR code
        qr.add_data(url)
        qr.make(fit=True)
        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")  
        file_path = f"qr_code_{url.split('/')[-1]}.png"
        print(f"QR code saved at: {file_path}")
        img.save(file_path)
        # return the qr code iimage and a message
        return img, f"QR code generated and saved at: {file_path}"
            
    except Exception as e:
        return f"Error generating QR code: {e}"



if __name__ == "__main__":
    url = "https://www.example.com"
    (img,qr_code_path) = generate_qr_code(url)
    print( img, qr_code_path)