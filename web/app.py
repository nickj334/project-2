"""
Nick Johnson's Flask API
"""

from flask import Flask, send_from_directory, request
import os
import configparser

app = Flask(__name__)


@app.before_request
def forbidden_check():
    '''
    Checking for forbidden URL's 
    '''
    requested_url = request.path

    if '..' in requested_url or '~' in requested_url:
        return send_from_directory('pages/', '403.html'), 403


@app.route("/")
def hello():
    return "UOCIS docker demo!\n"


@app.route("/<string:file>")
def trivia(file):
    if '~' in file or '..' in file:
        return send_from_directory('pages/', '403.html'), 403

    file_path = os.path.join('pages/', file)
    
    if not os.path.exists(file_path):
        return send_from_directory('pages/', '404.html'), 404
    
    return send_from_directory('pages/', file), 200


@app.errorhandler(404)
def not_found(e):
    return send_from_directory('pages/', '404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return send_from_directory('pages/', '403.html'), 403



'''
Inserting config parsing logic to attempt to get PORT and DEBUG values from
(1)credentials.ini first and then (2)default.ini second
'''
config = configparser.ConfigParser()
if config.read("credentials.ini"):
    port_value = config.getint("SERVER", "PORT")
    debug_value = config.getboolean("SERVER", "DEBUG")

elif config.read("default.ini"):
    port_value = config.getint("SERVER", "PORT")
    debug_value = config.getboolean("SERVER", "DEBUG")

if __name__ == "__main__":
    app.run(debug=debug_value, host='0.0.0.0', port=port_value)



