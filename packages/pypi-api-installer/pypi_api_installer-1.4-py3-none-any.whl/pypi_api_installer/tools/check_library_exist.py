import requests, json



def is_library_exist (library_name:str):
    """Verify the existence of the specified library on the PyPI (Python Package Index) website.
    
    Returns `True` if exists"""
    URL = f"https://pypi.org/pypi/{library_name}/json"
    content = requests.get(URL).text
    content = json.loads(content)

    if 'message' in content:
        if content['message'] == "Not Found":
            return False
    
    return True