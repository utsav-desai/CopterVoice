import mimetypes, json, glob
from codecs import encode
import glob
import requests
import warnings
warnings.filterwarnings('ignore')
import logging
import sys
import pandas as pd
import os
import time

# for debugging purpose
# http.client.HTTPSConnection.debuglevel = 1
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# uncoment this to set the https proxy if you're running it on the VM
# os.environ['https_proxy'] = 'http://proxy-weu.aze.michelin.com:80'

# converting the json combo output to a dataframe
def get_data_from_resp(json_dict:dict,response_name:str,columns:list)->dict:
    resp_dict = dict()
    json_resp = json_dict[response_name]
    car_model_count, combo_car_models = json_resp["result"]["car_models_matches"], json_resp["result"]["car_models"] if 'result' in json_resp else (None, None)
    
    resp_dict[columns[0]] = car_model_count
    resp_dict[columns[1]] = [f["tyre_dimensions"]['front']["tyresize"].replace(' ', '') for f in combo_car_models] if car_model_count else None
    resp_dict[columns[2]] = [r["tyre_dimensions"]['rear']["tyresize"].replace(' ', '') for r in combo_car_models] if car_model_count else None

    return resp_dict

def get_resp_dict(json_dict:dict)->dict:
    resp_info_dict = dict()
    if "tiresnap_resp" in json_dict:
        if json_dict["tiresnap_resp"]:
            ts_tire_dimensions = json_dict["tiresnap_resp"]["tire_dimension"]['summary'] 
            resp_info_dict['TS_Summary'] = ts_tire_dimensions if ts_tire_dimensions else None

    resp_info_dict['Image_Name'] = (json_dict["image_name"])

    if ("tiremotion_resp" in json_dict) and isinstance(json_dict["tiremotion_resp"], dict):
        if ('fault' not in json_dict["tiremotion_resp"]) and ('error' not in json_dict["tiremotion_resp"]):
            tm_details = get_data_from_resp(json_dict, "tiremotion_resp", ['TM_Model_Matchs','TM_Front', 'TM_Rear'] )
            resp_info_dict.update(tm_details)
    if ("combo_resp" in json_dict) and isinstance(json_dict["combo_resp"], dict):
        combo_resp = json_dict["combo_resp"]
        if not combo_resp['error']['code']:
            combo_details = get_data_from_resp(json_dict, "combo_resp", ['Combo_Model_Matchs','Combo_Front', 'Combo_Rear'] )
            resp_info_dict.update(combo_details)
    if resp_info_dict:
        return resp_info_dict


# a function to generate the access token for calling the combo API
def get_access_token(env=None):
    """
    Write a config file for env specific details
    """
    try:
        # url = 'https://dev.api.michelin.com/idp/v1/internal/oauth/token/accesstoken?grant_type=client_credentials'
        url = 'https://indus.api.michelin.com/idp/v1/internal/oauth/token/accesstoken?grant_type=client_credentials'

        # Set the OAuth2 endpoint and credentials
        token_url = url
        client_id = 'uFkxYQ1Ua0ktC5ARswbGQ7j0TllZUjD7'
        client_secret = 'dojCWDgyJPqrNYdh'

        # Set the grant type and scope
        grant_type = 'client_credentials'
        scope = 'rft-tire-size-recognition'

        # Make a request to the token endpoint to obtain an access token
        response = requests.post(
            token_url,
            auth=(client_id, client_secret),
            data={
                'grant_type': grant_type,
                'scope': scope,
            },
            verify= False
        )

        # Check if the request was successful
        if response.status_code == requests.codes.ok:
            # Extract the access token from the response
            access_token = response.json().get('access_token')
            # print(f'Access token: {access_token}')
            return access_token
        else:
            print(f'Failed to obtain access token: {response.text}')
    except Exception as e:
        print('Exception in getting access token==', e)
        return e

# function to call the api
def api_call(image_path):
    image_path = r'C:\Users\E080329\utsavtemp\PromptCraft-Robotics-main\chatgpt_airsim\images' + os.sep + image_path
    with open(image_path, 'rb') as image_file:
        url = 'https://indus.api.michelin.com/tire-size-recognition/v1/score?mode=debug'
        files = {'tire_image': image_file}
        body = {'requester_name': 'Mimetype', 'unique_request_id': 'debug-mimetype-123'}
        access_token = get_access_token()
        customer_combo_client_id = 'uFkxYQ1Ua0ktC5ARswbGQ7j0TllZUjD7'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'apikey': customer_combo_client_id,
            'Cache-Control': 'no-cache'
        }

        response = requests.post(url, headers=headers, files=files, data=body, verify=False)
        # print('status code', response.status_code)
        # print('response', response.text)
        return response.json()['tiremotion_resp']['result']['car_models'][0]['tyre_dimensions']


# function to call the api for the directory of images passed
def run(images_path):
  start_time = time.time()
  print('running', images_path)

  resp_dict_list = list()

  for image_name in os.listdir(images_path):
    print('running detections...', image_name)
    if image_name.endswith(('JPG', 'PNG', 'JPEG', 'jpg', 'png', 'jpeg')):
      path = os.path.join(images_path, image_name)
      response = api_call(path)
      response = json.loads(response)
      response['image_name'] = image_name
      resp_info_dict = get_resp_dict(response)
      resp_dict_list.append(resp_info_dict)

  resp_df = pd.DataFrame(resp_dict_list,columns=['Image_Name', 'TS_Summary', 'TM_Model_Matchs','TM_Front','TM_Rear', 
                                                 'Combo_Model_Matchs','Combo_Front', 'Combo_Rear'])
  
  end_time = time.time()-start_time
  print("--- %s seconds ---" % (time.time() - start_time))
  return resp_df, end_time
  
  
if __name__ == '__main__':
    # testing purpose
    df = api_call('simTyre.jpg')
    print(df)