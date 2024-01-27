import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL
import logging
server = Flask(__name__)

mysql = MySQL(server)

#config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER") 
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD") 
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB") 
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT")) 

secret = os.environ.get("JWT_SECRET")



def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now() + datetime.timedelta(hours=1),
            "iat": datetime.datetime.now(),
            "admin": authz
        },
        secret,
        algorithm="HS256",
    )




@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    #check db for username and password
    cursor = mysql.connection.cursor()
    res = cursor.execute("SELECT email, password FROM user WHERE email=%s", (auth.username, ))
    if res > 0:
        user_row = cursor.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else: 
            return createJWT(auth.username, secret, True), 200

    else:
        return "Not found !", 401
    

@server.route("/validate", methods=["POST"])
def validate():
    encoded = request.headers["Authorization"]
    logging.warning("this is the authorization header")
    logging.warning(encoded)
    logging.warning("#########")
    #check if there is any authorization headers
    if not encoded:
        logging.warning("the error occured because encoded does not exist")
        return "Unauthorized", 403


    #check for format validity and legitness of token
    try:
        encoded = encoded.split(" ")[1] 
        logging.warning("this is the encoded token")
        logging.warning("#################")
        logging.warning(encoded)
        decoded = jwt.decode(
            encoded, secret, algorithms=["HS256"]
        )
        logging.warning("this is the decoded token")
        logging.warning(decoded)
        return decoded, 200
    except:
        logging.warning("the error happened because the deconding did not go well")
        return "Unauthorized", 403




if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)
