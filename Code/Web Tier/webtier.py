from flask import Flask, render_template, Response, request
from flask_sse import sse
from flask_cors import CORS
import requests
import time
import hashlib

app = Flask(__name__)
#app.register_blueprint(sse, url_prefix='/stream')
CORS(app)

class AuthenticationService(object):
    def authenticate(self, username, password):
        if not username or not password:
            print("Empty username/password")
            return 'Username or password empty...'
        else:
            return self.send_request(username, password)

    def _encrypt_password(self,password):
        print("Encrypting...")
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        return encrypted_password

    def _connectToDatabase(self):
        print("Connecting to database...")
        connectUrl = "http://localhost:8080/connect"
        connectedResponse = requests.get(connectUrl)

        return connectedResponse.status_code

    def send_request(self, username, password):
        encrypted_password = self._encrypt_password(password)

        if self._connectToDatabase() == 200:
            print("Sending request to database...")

            url = 'http://localhost:8080/login/username={}&password={}'.format(username,encrypted_password)
            validity_message = requests.get(url).text

            print("RESPONSE: " + validity_message)

            return validity_message
        else:
            print("Could not connect to database.")
            return "Something went wrong."

class DealViewer(object):
    def getHistoricalData(self):

        # Get the parameters.
        # Start Date, End Date, Instrument, Counterparty

        # If Start date > End date wrong

<<<<<<< HEAD
        historicDataUrl = 'http://localhost:8080/showHistoricalData/'
=======
        historicDataUrl = 'http://localhost:8080/showHistoricalData/
>>>>>>> 57c465bccdea4e64ae62c451bc17d7a990eec057
        historicData = requests.get(historicDataUrl)

        # Format the data.

        # Perform calculations.
        # - Realised profit

        # Buy and sell averages

        # How do we return everything
        # If nothing?
        # Profit/Loss
        # Each Instrument Trade
        return "data"

def get_message():
    """this could be any function that blocks until data is ready"""
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

def bootapp():
    app.run(port=8090, threaded=True, host=('0.0.0.0'))

@app.route('/deals')
def forwardStream():
    r = requests.get('http://localhost:8080/streamTest', stream=True)
    def eventStream():
            for line in r.iter_lines( chunk_size=1):
                if line:
                    yield 'data:{}\n\n'.format(line.decode())
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/client/testservice')
def client_to_server():
    r = requests.get('http://localhost:8080/testservice')
    return Response(r.iter_lines(chunk_size=1), mimetype="text/json")

@app.route('/')
@app.route('/test')
def test():
    return "Connection to WebTier successful."

@app.route('/db')
def sendRequest():
    print("Sending request to database...")

    auth = AuthenticationService()
    response = auth.send_request("selvyn", "gradprog2016")

    return response

@app.route('/historicData')
def viewHistoric():
    print("Sending request to database...")

    dealDb = DealViewer()
    response = dealDb.getHistoricalData()

    return response

@app.route('/login', methods =['POST'])
def login():
    print("Login route accessed.")

    username = request.json['UN']['userName']
    password = request.json['PW']['userPassword']

    print("Got username and password.")

    auth = AuthenticationService()

    result = auth.authenticate(username, password)

    return result