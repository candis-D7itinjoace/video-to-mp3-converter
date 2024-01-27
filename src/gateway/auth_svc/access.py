import os, requests
import logging
def login(request):
    auth = request.authorization
    logging.warning("this is the auth variable")
    logging.warning(auth)
    logging.warning("####################")
    if not auth:
        return None, ("missing credentials", 401)
    basic_auth = (auth.username, auth.password)
    logging.warning("this is the basic_auth object")
    logging.warning(basic_auth)
    logging.warning("####################")
    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/login",
        auth=basic_auth,
        )
    if response.status_code == 200:
        return response.text, None
    else: 
        return None, (response.text, response.status_code)
