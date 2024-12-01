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
        try:
            response = requests.get(IP_API_URL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            ip_data = response.json()  # Get JSON data from response

            # Check if the response contains required data
            ip_info = {
                'ip': ip_data.get('ip'),
                'version': ip_data.get('version'),
                'city': ip_data.get('city'),
                'region': ip_data.get('region'),
                'country': ip_data.get('country_name'),
                'country_code': ip_data.get('country_code'),
                'latitude': ip_data.get('latitude'),
                'longitude': ip_data.get('longitude'),
                'asn': ip_data.get('asn'),
                'org': ip_data.get('org'),
            }

            return render_template('index.html', ip_info=ip_info)

        except Exception as e:
            # Log the error if needed
            app.logger.error(f"Error retrieving IP information: {str(e)}")
            # Return the template with an error message, with status 200
            return render_template('index.html', error='Error retrieving IP information'), 200

if __name__ == '__main__':
    app.run(debug=True)
