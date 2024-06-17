import requests


class Util:

    api_url = "https://api.murnitur.ai/api"
    endpoint = api_url + "/llm-evaluators/evaluations/save"

    def send_metrics(self, metrics: list, runs: list, headers: any):
        response = requests.post(
            self.endpoint, json={"data": metrics, "metrics": runs}, headers=headers
        )
        return response.status_code == 200 or response.status_code == 201

    def get_preset(self, name: str, api_key: str):
        try:
            response = requests.get(
                url=f"{self.api_url}/presets/sdk?name={name}",
                headers={"x-murnix-trace-token": api_key},
            )
            if response.status_code != 200:
                raise Exception(response.json()["message"])
            return response.status_code, response.json()
        except Exception as e:
            print(e)
            return response.status_code, None
