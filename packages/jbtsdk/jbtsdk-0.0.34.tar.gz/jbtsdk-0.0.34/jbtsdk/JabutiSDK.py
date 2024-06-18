import os
import requests
import json

class JabutiSDK():
    def __init__(self, api_url='', api_key=''):
        self.api_url = api_url if api_url else os.getenv("JBT_SDK_API_URL")
        self.api_key = api_key if api_key else os.getenv("JBT_SDK_API_KEY")
    
    def list_contexts(self):
        try:
            headers = {'x-api-key': self.api_key}
            response = requests.get(f"{self.api_url}/contexts", headers=headers, timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na listagem de conhecimentos.")
    
    def create_update_context(self, context_name, extension, file):
        try:
            headers = {'x-api-key': self.api_key}
            payload = {'context_name': context_name}
            with open(f"{context_name}.{extension}", "wb") as f:
                f.write(file)
            if(extension == "pdf"):
                files=[
                    ('file',(f"{context_name}.{extension}", open(f"{context_name}.{extension}", "rb"), f'application/{extension}'))
                ]
            elif(extension == "csv"):
                files=[
                    ('file',(f"{context_name}.{extension}", open(f"{context_name}.{extension}", "rb"), f'text/{extension}'))
                ]  
            response = requests.post(f"{self.api_url}/contexts", headers=headers, data=payload, files=files, timeout=60)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na criação ou atualização de conhecimento.")
    
    def delete_context(self, context_name):
        try:
            headers = {'x-api-key': self.api_key}
            payload = {'context_name': context_name}
            response = requests.delete(f"{self.api_url}/contexts", headers=headers, data=payload, timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha ao deletar conhecimento.")
        
    def fast_chat(self, input, username=None ,callbacks=[]):
        _payload = dict()
        _payload["input"] = str(input)
        if username:
            _payload["username"] = username
        try:
            headers = {'x-api-key': self.api_key}
            response = requests.post(self.api_url, data=json.dumps(_payload), headers=headers, timeout=60)
            if callbacks:
                for cb in callbacks:
                    cb.on_llm_end(response=response.text)
                    # cb.on_llm_new_token(token=response.text)
            # return response.content.decode('UTF-8')
            return response.text
            
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na execução.")
        
    async def async_fast_chat(self, input, username=None ,callbacks=[]):
        _payload = dict()
        _payload["input"] = str(input)
        if username:
            _payload["username"] = username
        try:
            headers = {'x-api-key': self.api_key}
            response = await requests.post(self.api_url, data=json.dumps(_payload), headers=headers, timeout=60)
            return response.content.decode('UTF-8')
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na execução.")
        
    def get_prompt(self, title):
        try:
            headers = {'x-api-key': self.api_key}
            payload = {'title': title}
            response = requests.post(f"{self.api_url}/prompt", headers=headers, data=json.dumps(payload), timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na listagem de comportamentos.")
    
    def list_prompts(self):
        try:
            headers = {'x-api-key': self.api_key}
            response = requests.get(f"{self.api_url}/prompts", headers=headers, timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na listagem de comportamentos.")
        
    def create_prompt(self, title, prompt):
        try:
            headers = {'x-api-key': self.api_key}
            payload = {'title': title, 'prompt': prompt}
            response = requests.post(f"{self.api_url}/prompts", headers=headers, data=json.dumps(payload), timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha na criação de comportamento.")
    
    def delete_prompt(self, title):
        try:
            headers = {'x-api-key': self.api_key}
            payload = {'title': title}
            response = requests.delete(f"{self.api_url}/prompts", headers=headers, data=json.dumps(payload), timeout=15)
            print(f"response: {response.text}")
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Falha ao deletar comportamento.")