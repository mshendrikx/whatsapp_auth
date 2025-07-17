import requests

def whatsapp_restart_session(base_url, api_key, session):
    
    headers = {'x-api-key': api_key} 
    
    url = f'{base_url}/session/restart/{session}'
    
    response = requests.get(url=url, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        return False
    

def whatsapp_send_message(base_url, api_key, session, contacts, content, content_type="string"):
    
    headers = {'x-api-key': api_key}    

    url = f'{base_url}/client/sendMessage/{session}'
    
    json_data = {'chatId': contacts,
             "contentType": content_type,
             'content': content
            }
    
    try:
        response = requests.get(url=url, headers=headers, json=json_data)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False
    
def whatsapp_convert_phone(int_phone):
    
    phone = str(int_phone)
    
    return phone.replace("+", "").replace("-", "").replace(" ", "") + '@c.us'