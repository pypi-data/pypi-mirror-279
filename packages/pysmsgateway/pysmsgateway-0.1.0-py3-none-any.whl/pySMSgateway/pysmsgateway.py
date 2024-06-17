import requests

class Pysmsgateway():
    def __init__(self,token:str,ip:str):
        self._sms_url = f"http://{ip}:8082"
        self._sms_token = token
# Sending a single message to a recipient
    def send_sms(self,recipient:str,message:str):
        payload = {"to": recipient, "message": message}
        return self._send(payload=payload)
# Sending different messages to different recipients 
    def send_sms_bulk(self,data:dict):
        for key, value in data.items:
            payload = {"to":key, "message":value}
            return self._send(payload=payload)
# Sending a single message to multiple recipient
    def send_sms_multiple(self,message:str,numbers:list):
        for number in numbers:
            payload = {"to":number, "message":message}
            return self._send(payload=payload)
# payload handler       
    def _send(self,payload:dict):
        headers = {
        "Authorization": f"{self._sms_token}",
        "Content-Type": "application/json"
        }
        try:
            with requests.Session() as session:
                response = session.post(self._sms_url, json=payload, headers=headers, verify=False)
                return True
        except Exception as e:
            return False
        
    