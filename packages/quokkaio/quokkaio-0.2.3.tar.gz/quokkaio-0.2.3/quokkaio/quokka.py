import requests
from time import sleep
from datetime import datetime
import logging

# Configure logging once at the module level
logger = logging.getLogger("Quokka")
logger.setLevel(level=logging.DEBUG)


def api_call(url, method='get', params=None, headers=None, timeout=30, files=None):
    """
    Makes an API call using the requests library.

    Args:
        url (str): The API endpoint.
        method (str): HTTP method ('get' or 'post'). Defaults to 'get'.
        params (dict): Parameters to send in the request.
        headers (dict): Headers to send with the request.
        timeout (int): Request timeout in seconds. Defaults to 30.
        files (dict): Files to send with the request.

    Returns:
        response (Response): The response object from the request.
    """
    try:
        method_types = ['get', 'post']
        if method not in method_types:
            raise ValueError("Invalid method type. Expected one of: %s" % method_types)

        if method == 'post':
            response = requests.post(url, data=params, headers=headers, timeout=timeout, files=files)
        else:
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        
        response.raise_for_status()
        return response

    except requests.exceptions.HTTPError as http_err:
        logger.debug(f"HTTP error occurred: {http_err}")
        logger.info(f"HTTP response content: {response.content if response else 'No response'}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.debug(f"Error connecting: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.debug(f"Timeout error: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.debug(f"An error occurred during the API request: {req_err}")

    return None

class Quokka:
    """
    A class to interact with the Quokka API.
    """

    def __init__(self, key):
        """
        Initializes the Quokka instance with an API key.

        Args:
            key (str): The API key.
        """
        self.api_key = key

    def push_scan(self, the_file, subgroup_ids):
        """
        Uploads an APK or IPA file to perform a scan.

        Args:
            the_file (str): The path to the APK/IPA file to upload.
            subgroup_ids (list): List of subgroup IDs.

        Returns:
            response_data (dict): The response data from the API.
            thePlatform (str): The platform ('android' or 'ios').
        """
        thePlatform = "ios" if the_file.lower().endswith("ipa") else "android"
        params = {'key': self.api_key, 'platform': thePlatform}
        if subgroup_ids != 0:
            params['subgroupIds'] = ','.join(subgroup_ids)

        url = 'https://emm.kryptowire.com/api/submit'
        with open(the_file, 'rb') as file:
            app_file = {'app': file}
            response = api_call(url, method='post', params=params, files=app_file)

        response_data = response.json() if response else None
        if response_data:
            return response_data, thePlatform
        else:
            logger.debug("No valid response received from the API")

    def get_sub_groups(self, the_group=None):
        """
        Retrieves a list of subgroups.

        Args:
            the_group (str, optional): A string to match against the list of subgroups.
                                       If not provided, prints the list of subgroups.

        Returns:
            group_id (str): The ID of the matching subgroup if found.
        """
        url = "https://api.kryptowire.com/group-admin/sub-groups"
        params = {'key': self.api_key}
        headers = {'Accept': 'application/json'}
        response = api_call(url, method='get', params=params, headers=headers)
        response_data = response.json() if response else None

        if response_data:
            if not the_group:
                for r in response_data:
                    logger.info('{} : {}'.format(r['id'], r['name']))
            else:
                for r in response_data:
                    if r['name'].lower() == the_group.lower():
                        return r['id']
        else:
            logger.debug("No valid response received from the API")
        
        return None

    def wait_for_scan_complete(self, uuid, maxWaitTime=0):
        """
        Waits for a scan to complete.

        Args:
            uuid (str): The unique ID of the scan.
            maxWaitTime (int): Maximum wait time in minutes. Defaults to 0 (no limit).

        Returns:
            bool: True if the scan completes successfully.
        """
        status = 'processing'
        count = 0
        while status == 'processing':
            if maxWaitTime > 0 and count >= maxWaitTime:
                raise Exception("Scan did not complete within the maximum wait time.")
            url = 'https://api.kryptowire.com/api/status'
            params = {'key': self.api_key, 'uuid': uuid}
            response = api_call(url, method='get', params=params)
            response_data = response.json() if response else None

            if response_data:
                logger.info(response_data)
                status = response_data['status']
            else:
                logger.debug("No valid response received from the API")

            sleep(60)
            count += 1
        
        return True

    def download_pdf(self, uuid):
        """
        Downloads the scan results as a PDF file.

        Args:
            uuid (str): The unique ID of the scan.

        Returns:
            None
        """
        params = {'key': self.api_key, 'uuid': uuid, 'regeneratePDF': True}
        url = 'https://emm.kryptowire.com/api/results/pdf'
        response = api_call(url, method='get', params=params)

        if response:
            with open(f"pdf{uuid}.pdf", 'wb') as pdf:
                pdf.write(response.content)
            logger.info(f"File pdf{uuid}.pdf downloaded")

    def get_app_issue(self, uuid):
        """
        Retrieves app issues in JSON format.

        Args:
            uuid (str): The unique ID of the app test run.

        Returns:
            str: The response text from the API.
        """
        url = "https://api.kryptowire.com/app-issues/parsed/"
        params = {'key': self.api_key, 'uuid': uuid}
        response = api_call(url, method='get', params=params)
        return response.text if response else None
    
    def get_results(self, start_date):
        """
        Retrieves specified results in JSON format.

        Args:
            start_date (datetime): The date to start retrieving results from.

        Returns:
            str: The response text from the API.
        """
        days = (datetime.today() - start_date).days
        url = "https://api.kryptowire.com/api/analytics/"
        params = {'key': self.api_key, 'range': days, 'type': 'days'}
        response = api_call(url, method='get', params=params)
        return response.text if response else None
    
    def get_apps(self, start_date, end_date):
        """
        Retrieves submitted apps in JSON format.

        Args:
            start_date (datetime): The start date for retrieving results.
            end_date (datetime): The end date for retrieving results.

        Returns:
            str: The response text from the API.
        """
        url = "https://api.kryptowire.com/api/submitted-apps/"
        params = {
            'key': self.api_key,
            'startDate': start_date.strftime("%Y-%m-%d"),
            'endDate': end_date.strftime("%Y-%m-%d")
        }
        response = api_call(url, method='get', params=params)
        return response.text if response else None
    
    def get_users(self, isCompressed=False):
        """
        Users can request that the file is sent as either a CSV or as a compressed file. 

        Args:
            isCompressed (boolean): Determines whether to send a compressed file

        Returns:
            bool: True if file is successfully saved, False otherwise.
        """
        url = "https://api.kryptowire.com/api/group-admin/users-csv"
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        params = {
            'key': self.api_key,
            'isCompressed': isCompressed
        }
        response = api_call(url, method='get', params=params)
        if response:
            content_type = response.headers.get('Content-Type')
            if 'text/csv' in content_type:
                # Handle CSV file
                file_path = f'{date_string}-group_user_data.csv'
                with open(file_path, 'w') as file:
                    file.write(response.text)
                logger.info(f"CSV file has been saved as {file_path}")
                return True
            elif 'application/zip' in content_type:
                # Handle compressed file
                file_path = f'{date_string}-group_user_data.zip'
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                logger.info(f"Compressed file has been saved as {file_path}")
                return True
            else:
                logger.error(f"Unknown Content Error: {content_type}")
                return False
        else:
            logger.error(f"Error: {response}")
            return False
        
    def get_auditLogs(self, startDate, endDate, isCompressed=False, pageType='audit'):
        """
        Users can request the Audit Log CSV which will be processed in the background.

        Args:
            isCompressed (boolean): Determines whether to send a compressed file
            pageType (str): The type of CSV requested. For audit log data users should request "audit"
            start_date (datetime): The start date for retrieving results.
            end_date (datetime): The end date for retrieving results.

        Returns:
            bool: True if file is successfully saved, False otherwise.
        """
        url = "https://api.kryptowire.com/api/csv-request"
        params = {
            'key': self.api_key,
            'isCompressed': isCompressed,
            'pageType': pageType,
            'startDate': startDate,
            'endDate': endDate
        }
        response = api_call(url, method='post', params=params)
        if response:
            logger.info("Email will be sent with download link")
            return True 
        else:
            logger.error("Issue retrieving audit results") 
            return False