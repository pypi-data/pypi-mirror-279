import sys



def is_user_have_library (lib_name:str):
    """Check whether the user have the library in the current site-packages or not"""

    if lib_name in dict(sys.modules):
        return True
    else:
        return False