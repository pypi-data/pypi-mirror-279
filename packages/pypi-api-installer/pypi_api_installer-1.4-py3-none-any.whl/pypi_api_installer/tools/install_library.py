import requests, json



def install_library (lib_name:str, version:str, download_location_path:str):
    URL = f"https://pypi.org/pypi/{lib_name}/json"
    content = requests.get(URL).text
    content = json.loads(content)

    releases = content['releases']

    download_url = releases[f'{version}'][0]['url']

    download_response = requests.get(download_url, stream=True)
    download_response.raise_for_status()

    with open(f"{download_location_path}/{lib_name}.tar.gz", 'wb') as file:
        for chunk in download_response.iter_content():
            file.write(chunk)

if __name__ == "__main__":
    install_library("googletrans", "2.31.0", "./")