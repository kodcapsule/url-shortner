
import validators


def validate_url(url):
         
    """
    Validates if the given string is a properly formatted URL.
    
    Args:
        url (str): The URL string to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
        str: The original URL if valid, or an error message if invalid
    """
    if url is None or url == "":
        return False, "URL cannot be None or empty"
    try:
        # Use validators library to check if the URL is valid
        # This will also check for common URL formats (http, https, etc.)
        if not validators.url(url):
            return False, f'Invalid URL format: {url}'
    except Exception as e:
            return False, f'Invalid url Format: {e}'

    return validators.url(url), url