import requests, json

def get_library_dependency_names(lib_name:str):
    """Get the library's required packages and return a list of their names."""
    package_reqs = []

    try:
        get_dpdns = json.loads(requests.get(f"https://pypi.org/pypi/{lib_name}/json").text)['info']['requires_dist']
    except:
        raise Exception("There was an error while trying to fetch dependencies.")

    # If not dpnts
    if get_dpdns is None: return []

    # Index dpnts
    for pkn in get_dpdns:
        full_name = ""
        complete_getten_litters = True
        for n in pkn:
            if n != "(" and n != ")" and n != ";" and complete_getten_litters:
                full_name = full_name + n
            else:
                complete_getten_litters = False
        package_reqs.append(full_name.replace(" ", ""))
    
    return package_reqs

if __name__ == "__main__":
    print(get_library_dependency_names("requests"))