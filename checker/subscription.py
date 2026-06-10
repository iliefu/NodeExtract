import base64
import requests
import logging

def fetch(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        text = response.text.strip()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch subscription from {url}: {e}")
        return []
    
    # Try base64 decoding
    try:
        # Proper base64 padding
        padding = len(text) % 4
        if padding:
            text = text + "=" * (4 - padding)
        text = base64.b64decode(text).decode()
    except (ValueError, UnicodeDecodeError):
        pass  # Not base64 encoded, use as-is
    
    return [x.strip() for x in text.splitlines() if x.strip()]
