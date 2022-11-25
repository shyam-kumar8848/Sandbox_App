import frappe
from frappe import _
import requests
import json
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def get_access_token(x_api_key, x_api_secret):
    try:
        setting = frappe.get_doc('Sandbox')
        url = setting.sandbox_auth_url
        #print(url)
        headers = {
            'accept': 'application/json',
            'x-api-key': x_api_key,
            'x-api-secret': x_api_secret,
            'x-api-version': setting.x_api_version
        }
        response = requests.request("POST", url, headers = headers)
        data = response.json()
        access_token = data['access_token']
        #print(access_token)
        return({'status' : 'success', 'access_token' : access_token})
    except Exception as e:
        return({'status' : 'failure', 'data' : 'Authentication Error. Please check Sandbox'})