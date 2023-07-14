import sys
import requests
import json
import os
import yaml
import warnings
warnings.filterwarnings("ignore")
CONFIG_PATH = "config.yml"

with open(CONFIG_PATH, 'r') as f:
    config_yml = yaml.safe_load(f)


##
##    function to obtain a new OAuth 2.0 token from the authentication server
##
def get_new_token():
    auth_server_url = config_yml["token"]["auth_server_url"]
    client_id = config_yml["token"]["client_id"]
    client_secret = config_yml["token"]["client_secret"]

    token_req_payload = {'grant_type': 'client_credentials'}

    token_response = requests.post(auth_server_url,
    data=token_req_payload, verify=False, allow_redirects=False,
    auth=(client_id, client_secret))
    # print(token_response.status_code)
    if token_response.status_code !=200:
        print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
        sys.exit(1)

    # print("Successfuly obtained a new token")
    tokens = json.loads(token_response.text)
    return tokens['access_token']

##
## 	obtain a token before calling the API for the first time
##

chat_history = []

def getAns(prompt):
    token = get_new_token()
    
    url = config_yml["api_url"]
    # os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\E080329\utsavtemp\Azure-openai-chatgpt-Sample\cert\api.openai.crt'
    # os.environ['REQUESTS_CA_BUNDLE'] = r'C:\Users\E080329\utsavtemp\Azure-openai-chatgpt-Sample\cert\sase-mob-sslfwd-trust-ca.michelin.crt'
    
    payload = json.dumps({
        "prompt": prompt,
        "temperature": float(0.2),
        "top_p": float(1),
        "max_tokens": int(3000)
    })

    headers = {
        'apikey': config_yml["headers"]["apikey"],
        'Content-Type': config_yml["headers"]["content_type"],
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify = False)

    if response.status_code != 200:
        headers['Authorization'] = f'Bearer {get_new_token()}'
        response = requests.request("POST", url, headers=headers, data=payload)

    print(response)
    #return response.json()['choices'][0]['text'].replace('\n','').replace(' .','.').strip()

if __name__ == '__main__':
    prompt = ''
    while prompt != 'exit' and prompt != 'quit':
        prompt = input('Prompt: ')
        print(getAns(prompt))