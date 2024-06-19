import re

def parse_package_string(package_string):
    """
    Parse a package string with version constraints to extract the package name, minimum version, and maximum version.

    Args:
        package_string (str): The package string, e.g., "charset-normalizer<4,>=2".

    Returns:
        tuple: A tuple containing the package name (str), minimum version (str or None), and maximum version (str or None).
    """
    package_name = re.match(r"^[a-zA-Z0-9_-]+", package_string).group(0)
    min_version = None
    max_version = None
    
    min_version_match = re.search(r">=([0-9.]+)", package_string)
    max_version_match = re.search(r"<([0-9.]+)", package_string)
    
    if min_version_match:
        min_version = min_version_match.group(1)
    if max_version_match:
        max_version = max_version_match.group(1)
    
    return package_name, min_version, max_version
