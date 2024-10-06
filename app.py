from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Define the API endpoint for fetching the public IP info
IP_API_URL = "https://ipapi.co/json/"

@app.route('/')
def home():
    # Redirect to the /get_ip_info route
    return redirect(url_for('get_ip_info'))

@app.route('/get_ip_info', methods=['POST', 'GET'])
def get_ip_info():
    # If the method is GET, fetch the IP info
    if request.method == 'GET':
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
