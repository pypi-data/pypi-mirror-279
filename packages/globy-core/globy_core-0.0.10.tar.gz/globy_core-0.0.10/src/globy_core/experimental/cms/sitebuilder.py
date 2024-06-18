import requests
from os import environ

class Site:
    def __init__(self, user_id, full_name):
        self.user_id = user_id
        self.full_name = full_name
        self.data = {
        'site_name': user_id,
        'user_id': user_id,
        'full_name': full_name,
        'controls': 'none',
    }


class SiteBuilder:
    def __init__(self):
        self.wordpress_url = 'https://www.globy.ai'
        self.api_endpoint = f'{self.wordpress_url}/wp-json/custom/v1/create_site/'
        self.username = environ.get('WP_USERNAME')
        self.password = environ.get('WP_PASSWORD')
        self.auth = (self.username, self.password)
        self.headers = {
            'Secret-Key': environ.get("WP_SECRET")
        }

    def create_wordpress_site(self, user_id, full_name):
        site = Site(user_id, full_name)
        response = requests.post(self.api_endpoint, auth=self.auth, json=site.data, headers=headers)
        return response.json()
    
def load_globy_blobs() -> tuple:
    """
    Loads controls_html and globy_js from local files
    """
    with open('controls_html.txt') as f:
        controls_html = f.read()
    with open('globy_js.txt') as f:
        globy_js = f.read()
    return controls_html, globy_js
