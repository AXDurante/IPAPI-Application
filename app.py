from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Define the API endpoint for fetching the public IP info
IP_API_URL = "https://ipapi.co/json/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_ip_info', methods=['POST'])
def get_ip_info():
    # Send a GET request to fetch the IP info
    response = requests.get(IP_API_URL).json()

    # Check if the response contains required data
    if response:
        ip_info = {
            'ip': response.get('ip'),
            'version': response.get('version'),
            'city': response.get('city'),
            'region': response.get('region'),
            'country': response.get('country_name'),
            'country_code': response.get('country_code'),
            'latitude': response.get('latitude'),
            'longitude': response.get('longitude'),
            'asn': response.get('asn'),
            'org': response.get('org'),
        }
        return render_template('index.html', ip_info=ip_info)
    else:
        error_message = "Could not retrieve IP information."
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
