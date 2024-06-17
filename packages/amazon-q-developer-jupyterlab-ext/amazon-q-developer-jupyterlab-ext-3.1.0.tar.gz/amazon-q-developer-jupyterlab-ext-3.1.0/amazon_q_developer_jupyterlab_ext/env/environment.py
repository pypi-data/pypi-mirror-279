import json
import logging
import os

import aiohttp
from aiohttp import ClientTimeout
from packaging.version import Version
from amazon_q_developer_jupyterlab_ext.client.sagemaker.client import get_sagemaker_client
from amazon_q_developer_jupyterlab_ext.constants import CURRENT_VERSION, CODEWHISPERER_PYPI_JSON_URL, NEW_VERSION_USER_MESSAGE, \
    CONSUMER_ENV_KEY, CONSUMER_ENV_VALUE_GLUE_STUDIO

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class Environment:
    SM_STUDIO = "SageMaker Studio"
    SM_STUDIO_SSO = "SageMaker Studio SSO"
    JUPYTER_OSS = "Jupyter OSS"
    GLUE_STUDIO_NOTEBOOK = "Glue Studio Notebook"
    MD = "MD"
    _cached_env = None

    @staticmethod
    async def get_update_notification():
        try:
            # Glue Studio environment doesn't want any update and update notification
            is_sm_studio = await Environment.is_sm_studio()
            if Environment.is_glue_studio() or is_sm_studio:
                return "", ""

            # Get the URL from environment variable or fall back to default
            url = os.environ.get("JSON_URL", CODEWHISPERER_PYPI_JSON_URL)

            # Download the JSON data
            async with aiohttp.ClientSession() as session:
                # Define the timeout duration (in seconds)
                timeout_duration = 2  # Timeout after 2 seconds

                # Create a ClientTimeout object
                timeout = ClientTimeout(total=timeout_duration)

                async with session.get(url, timeout=timeout) as response:
                    response.raise_for_status()
                    data = await response.json()

            # Get the latest version and launch date
            latest_version = data["info"]["version"]

            # Compare the current version with the latest version
            if Version(latest_version) > Version(CURRENT_VERSION):
                return NEW_VERSION_USER_MESSAGE.format(latest_version), latest_version
            else:
                return "", ""
        except Exception as e:
            print(f"Error: {e}")
            return "", ""

    @staticmethod
    async def get_environment():
        if Environment._cached_env is None:
            logging.info("Detecting environment for the first time")
            Environment._cached_env = await Environment._detect_environment()
        logging.info(f"Environment is {Environment._cached_env}")
        return Environment._cached_env

    @staticmethod
    async def _detect_environment():
        env = Environment.JUPYTER_OSS
        try:
            if Environment.is_glue_studio():
                return Environment.GLUE_STUDIO_NOTEBOOK

            with open('/opt/ml/metadata/resource-metadata.json', 'r') as f:
                data = json.load(f)
                if 'AdditionalMetadata' in data and 'DataZoneScopeName' in data['AdditionalMetadata']:
                    env = Environment.MD
                elif 'ResourceArn' in data:
                    sm_domain_id = data['DomainId']
                    logging.info(f"DomainId - {sm_domain_id}")
                    sm_client = get_sagemaker_client()
                    try:
                        domain_details = await sm_client.describe_domain(sm_domain_id)
                        logging.info(f"Studio domain level details: {domain_details}")
                        if (domain_details.get('AuthMode') == "SSO"
                                and (domain_details.get('DomainSettings') is not None
                                     and domain_details.get('DomainSettings').get('AmazonQSettings') is not None
                                     and domain_details.get('DomainSettings').get('AmazonQSettings').get('Status') == 'ENABLED')):
                            env = Environment.SM_STUDIO_SSO
                        else:
                            env = Environment.SM_STUDIO
                    except Exception as e:
                        logging.info(f"Failed to get Studio domain details {str(e)}")
                        env = Environment.SM_STUDIO
        except Exception as e:
            logging.error(f"Error detecting environment: {str(e)}")
        return env

    @staticmethod
    def is_glue_studio():
        return CONSUMER_ENV_KEY in os.environ and os.environ.get(CONSUMER_ENV_KEY) == CONSUMER_ENV_VALUE_GLUE_STUDIO

    @staticmethod
    async def is_sm_studio():
        return await Environment.get_environment() == Environment.SM_STUDIO
