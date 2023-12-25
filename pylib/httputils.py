import re

class RestApiResponse:
    def __init__(self, content, status_code):
        self.content = content
        self.status_code = status_code

def check_email_address(address:str) -> bool:
    address = address.lower()
    email_validate_pattern = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"
    if re.match(email_validate_pattern, address):
        return True
    else:
        return False
