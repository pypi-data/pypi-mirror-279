import requests

class Neurum:
    def __init__(self, key):
        self.key = key
        self.url = "https://api.rnilaweera.lk/api/v1/user/mixtral"
        self.headers = {"Authorization": f"Bearer rsnai_KCLojKDTOY4b1hNeNFIwFaqN"}
    
    def generate(self, prompt):
        if self.key=="vansh":
            payload = {"prompt": prompt}
            response = requests.post(self.url, json=payload, headers=self.headers)
            return response.json()  # Assuming the API returns JSON; adjust if needed
        else:
            print('failedddddd bruhhhh!!!!')