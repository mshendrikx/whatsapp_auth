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
   
    contatc_fail = []
    for contact in contacts:        
        chatid = [whatsapp_convert_phone(contact)]
        json_data = {'chatId': chatid,
                 "contentType": content_type,
                 'content': content
                }
        try:
            response = requests.post(url=url, headers=headers, json=json_data)
            if response.status_code != 200 or response.status_code != 500:
                contatc_fail.append(contact)
        except Exception as e:
            contatc_fail.append(contact)
    
    return contatc_fail
    
def whatsapp_convert_phone(int_phone):
    
    phone = str(int_phone)
    
    return phone.replace("+", "").replace("-", "").replace(" ", "") + '@c.us'