import frappe
from frappe import _
import requests
from frappe.model.document import Document
from sandbox.API.access_token_api import get_access_token


@frappe.whitelist(allow_guest=True)
def get_employee_details(**kwargs):
    try:
        pan = kwargs.get('pan')
        adhar = kwargs.get('adhar')
        x_api_key = frappe.request.headers.get("x-api-key")
        x_api_secret = frappe.request.headers.get("x-api-secret")

        authorization = get_access_token(x_api_key, x_api_secret)
        if (authorization['status'] == 'failure'):
            return(authorization)

        setting = frappe.get_doc('Sandbox')
        url = 'https://api.sandbox.co.in/pans/'
        url=f"{url}{pan}/pan-aadhaar-status?aadhaar_number={adhar}" 
        
        headers = {
            "Authorization": authorization['access_token'],
            "x-api-key": setting.x_api_key,
            "x-api-version": setting.x_api_version
        }
        response = requests.request("GET",url, headers=headers)
        json_response = response.json()
        response_data = json_response['data']
        print('Server Response',response_data)
        return({'status' : 'success', 'data' : response_data})
    except Exception as e:
        return({'status' : 'failure', 'data' : 'Error in fetching data from API'})