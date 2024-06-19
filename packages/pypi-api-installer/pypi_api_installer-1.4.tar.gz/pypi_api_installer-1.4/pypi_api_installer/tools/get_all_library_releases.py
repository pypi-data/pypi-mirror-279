import requests, json



def get_all_releases_of_library (library_name:str):
    URL = f"https://pypi.org/pypi/{library_name}/json"
    content = requests.get(URL).text
    content = json.loads(content)

    releases = content['releases']

    rel = []
    for i in releases:
        rel.append(i)

    return rel


if __name__ == "__main__":
    print(get_all_releases_of_library("requests"))