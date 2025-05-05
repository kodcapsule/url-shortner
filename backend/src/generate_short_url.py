
import pyshorteners
import json
def generate_short_url(original_url):
    """
    Generates a short URL for the given original URL.
    
    Args:
        original_url (str): The original URL to shorten
        
    Returns:
        str: The generated short URL
    """
    try:
        # Create an instance of the Bitly API client
        shortner = pyshorteners.Shortener()      
        # Shorten the URL using Bitly
        short_url = shortner.tinyurl.short(original_url)
        return short_url
    except Exception as e:
        print(f"Error generating short URL: {e}")
        return json.dumps({'error': str(e)})