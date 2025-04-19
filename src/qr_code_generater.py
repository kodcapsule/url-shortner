import qrcode





def generate_qr_code(original_url):
    """
    Generates a QR code for the given original URL.
    
    Args:
        original_url (str): The original URL to generate a QR code for
        
    Returns:
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
        qr.add_data(original_url)
        qr.make(fit=True)
        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")  
        file_path = f"qr_code_{original_url.split('/')[-1]}.png"
        print(f"QR code saved at: {file_path}")
        img.save(file_path)
        return file_path
    
    except Exception as e:
        return f"Error generating QR code: {e}"


# Example usage
if __name__ == "__main__":
    original_url = "https://www.example.com"
    qr_code_path = generate_qr_code(original_url)
    print(f"QR code generated and saved at: {qr_code_path}")