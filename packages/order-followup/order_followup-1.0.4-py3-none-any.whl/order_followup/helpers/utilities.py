import os

def get_base_url(url:str)-> str:
    """
    Returns a url without the trailing slash (/)
    @param: url: the url to process
    """
    base = url.strip()
    if base[-1] == '/':
        base = base[:-1]
    return base  


def get_shopify_api_credentials()-> dict:
    """
    Return Shopify Admin API credentials as a dictionary. 
    WARNING: you must store the credentials as OS environment variables.
    """
    SHOPIFY_API_KEY                 = os.environ.get("SHOPIFY_API_KEY")
    SHOPIFY_ADMIN_API_ACCESS_TOKEN  = os.environ.get("SHOPIFY_ADMIN_API_ACCESS_TOKEN")
    SHOPIFY_API_SECRET_KEY          = os.environ.get("SHOPIFY_API_SECRET_KEY")
    if not all([SHOPIFY_API_KEY, SHOPIFY_ADMIN_API_ACCESS_TOKEN, SHOPIFY_API_SECRET_KEY]):
        raise ValueError("One or more required Shopify API credentials was not found in your OS environment variables. Please check them and try again.")
 
    return {
        "SHOPIFY_API_KEY": SHOPIFY_API_KEY, 
        "SHOPIFY_ADMIN_API_ACCESS_TOKEN": SHOPIFY_ADMIN_API_ACCESS_TOKEN, 
        "SHOPIFY_API_SECRET_KEY": SHOPIFY_API_SECRET_KEY
    }
    
