import requests
api_url = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(organism_id:9606)"
response = requests.get(api_url)
response.json()

def print_response():
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {response.text}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_response()

