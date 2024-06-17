## Authivate (Python SDK)

This is the official python package for the [Authivate](https://authivate.com) service.

Authivate is an easy-to-use User Authentication and Management service.

### Install
To Install, using pip
```sh
pip install authivate
```

Using poetry
```shell
poetry add authivate
```

### Example Usage

```python
from authivate import  Authivate, AuthivateConfig
from pprint import pprint

def add_user_to_waitlist(authivate: Authivate):
    # Adds a user to the waitlist
    response = authivate.add_user_to_waitlist(
        email_address="user@example.com"
    )
    if response.was_successful:
        print("User added to waitlist")
        pprint(response.json_data)
    else:
        print(f"Error: {response.status_code} - {response.json_data}")


# Initialize AuthivateConfig
authivate_config = AuthivateConfig(api_key="your-api-key", project_id="project-id")


# Create an instance of Authivate
authivate_instance = Authivate(config=authivate_config)

# Adds a user to the waitlist
'''Response
{'message': 'Yah!, you are now on the waitlist for {Project name}. Please confirm your email to seal your spot'}
 '''
add_user_to_waitlist(authivate_instance)
```
### PS
If you have used authivate before now June 17, 2024, what you think of authivate is definitely different from what it is now.
it was completely rewritten to support only waitlist collection.

Thanks,
Peter.