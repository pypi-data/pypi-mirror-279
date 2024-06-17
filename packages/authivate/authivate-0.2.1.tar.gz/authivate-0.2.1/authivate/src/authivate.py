from pprint import pprint

import requests

from authivate.src.utils.authivate_config import AuthivateConfig
from authivate.src.utils.authivate_response import AuthivateResponse


class Authivate:
    def __init__(self, config: AuthivateConfig):
        self.config = config
        self._headers = {"Authorization": f"Bearer {config.api_key}"}
        self.client = requests.Session()

    def post_request(self, uri, body):
        try:
            response = self.client.post(uri, headers=self._headers, json=body)
            response.raise_for_status()
            return AuthivateResponse(response.status_code, response.json())
        except requests.exceptions.HTTPError as err:
            status_code = err.response.status_code
            json_data = (
                err.response.json()
                if "application/json" in err.response.headers.get("content-type", "")
                else None
            )
            return AuthivateResponse(status_code, json_data)
        except Exception as e:
            return AuthivateResponse(500, {"error": str(e)})

    def add_user_to_waitlist(self, **kwargs):
        url = f"api/v1/p/project/{self.config.project_id}/user_records/"
        body = {
            **kwargs,
        }
        uri = f"https://{self.config.host}/{url}"
        response = self.post_request(uri, body)
        return response


# Example Usage
if __name__ == "__main__":

    # Initialize AuthivateConfig
    authivate_config = AuthivateConfig(api_key="your-api-key", project_id="project-id")

    # Create an instance of Authivate
    authivate_instance = Authivate(config=authivate_config)

    # Add user to waitlist
    """Response
    {'message': 'Yah!, you are now on the waitlist for {project name}. Please confirm your email to seal your spot'}
    """

    authivate_instance.add_user_to_waitlist(authivate_instance)
