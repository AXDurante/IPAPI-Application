from flask import Flask, render_template, request, redirect, url_for
import requests
from requests.exceptions import RequestException
import time
from functools import lru_cache
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
IP_API_URL = "https://ipapi.co/json/"
REQUEST_TIMEOUT = 5  # seconds
CACHE_TIMEOUT = 300  # 5 minutes in seconds
MAX_REQUESTS = 30  # Maximum requests per minute
HEADERS = {
    'User-Agent': 'YourApp/1.0'
}

# Rate limiting setup
request_timestamps = []

def is_rate_limited():
    """Check if we've exceeded our rate limit"""
    global request_timestamps
    now = datetime.now()
    
    # Remove timestamps older than 1 minute
    request_timestamps = [ts for ts in request_timestamps 
                        if now - ts < timedelta(minutes=1)]
    
    # Check if we've exceeded our limit
    if len(request_timestamps) >= MAX_REQUESTS:
        return True
    
    # Add current timestamp
    request_timestamps.append(now)
    return False

@lru_cache(maxsize=1024)
def get_cached_ip_info():
    """Fetch IP info with caching"""
    response = requests.get(
        IP_API_URL,
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()

# Function to clear cache entry after timeout
def get_ip_info_with_timeout():
    """Get IP info with cache timeout"""
    current_time = time.time()
    
    # Get the cached function's cache_info
    cache_info = get_cached_ip_info.cache_info()
    
    # If cache exists and is older than timeout, clear it
    if cache_info.currsize > 0:
        # Clear the cache if it's older than CACHE_TIMEOUT
        get_cached_ip_info.cache_clear()
    
    return get_cached_ip_info()

@app.route('/')
def home():
    return redirect(url_for('get_ip_info'))

@app.route('/get_ip_info', methods=['POST', 'GET'])
def get_ip_info():
    if request.method == 'GET':
        try:
            # Check rate limiting
            if is_rate_limited():
                app.logger.warning("Rate limit reached")
                return render_template('index.html',
                    error='Too many requests. Please try again in a minute.'), 429

            # Try to get cached data first
            try:
                ip_data = get_ip_info_with_timeout()
            except Exception as cache_error:
                app.logger.error(f"Cache error: {str(cache_error)}")
                return render_template('index.html',
                    error='Service temporarily unavailable.'), 200

            # Extract IP info
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

        except requests.exceptions.Timeout:
            app.logger.error("Timeout while fetching IP information")
            return render_template('index.html',
                error='Service is taking too long to respond. Please try again.'), 200

        except requests.exceptions.TooManyRedirects:
            app.logger.error("Too many redirects")
            return render_template('index.html',
                error='Service configuration error.'), 200

        except requests.exceptions.RequestException as e:
            app.logger.error(f"Request error: {str(e)}")
            return render_template('index.html',
                error='Error retrieving IP information.'), 200

        except Exception as e:
            app.logger.error(f"Unexpected error: {str(e)}")
            return render_template('index.html',
                error='An unexpected error occurred.'), 200

if __name__ == '__main__':
    app.run(debug=True)
