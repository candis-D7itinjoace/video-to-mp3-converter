import os, requests
import logging

def token(request):
    if not "Authorization" in request.headers:
        logging.warning("the error happened because there is no authorization header")
        return None, ("Unauthorized", 403)
    
    token = request.headers["Authorization"]
    logging.warning("this is the access token")
    logging.warning(token)

    if not token:
        logging.warning("the error happened because there is no token in the header authorization")
        return None, ("Unauthorized", 403)  
    
    response = requests.post(
        f"http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate",
        headers={"Authorization": token},
    )
    logging.warning("this is the response object")
    logging.warning(response)

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
