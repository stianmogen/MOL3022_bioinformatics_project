import requests
api_url = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(organism_id:9940)"
api_url2 = "https://rest.uniprot.org/uniprotkb/search?query=(reviewed:true)%20AND%20(gene_exact:APOH_HUMAN)"
api_url3 = "https://rest.uniprot.org/uniprotkb/search?query=gene_exact:APOH&format=json"
response = requests.get(api_url)
response.json()

#350	APOH 	apolipoprotein H (beta-2-glycoprotein I)
def print_response():
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {response.text}')  # Press ⌘F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_response()

