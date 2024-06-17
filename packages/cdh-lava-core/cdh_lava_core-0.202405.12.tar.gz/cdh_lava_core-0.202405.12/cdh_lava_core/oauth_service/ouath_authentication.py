import json
import base64
import os
from urllib.parse import urlencode, quote_plus, urlparse, urlunparse
from flask import request, redirect, make_response
# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)
from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

class OAuthAuthentication:
    
    @staticmethod
    def get_login_redirect_response(config):
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_login_redirect_response"):
            try:

                tenant = config.get("az_sub_tenant_id")
                client_id = config.get("az_sub_web_client_id")

                # Define the base URL for Azure AD authorization
                base_url = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"

                current_url = request.url

                # Define your data
                data = {"url": current_url}

                # Convert the data to JSON
                json_data = json.dumps(data)

                # Encode the JSON data as bytes
                json_bytes = json_data.encode("utf-8")

                # Base64 encode the bytes
                base64_data = base64.urlsafe_b64encode(json_bytes)

                # Convert the base64 bytes to a string
                base64_string = base64_data.decode("utf-8")

                callback_url = OAuth.get_callback_url()

                state = base64_string

                params = {
                    "client_id": client_id,
                    "response_type": "code",
                    "redirect_uri": callback_url,
                    "response_mode": "form_post",
                    "scope": "openid",
                    "state": state,
                }

                # URL encode the parameters
                params_encoded = urlencode(params, quote_via=quote_plus)

                # Construct the full Azure AD authorization URL
                auth_url = f"{base_url}?{params_encoded}"

                if request.scheme == "https":
                    secure = True
                else:
                    secure = False

                try:
                    response = make_response(redirect(auth_url))
                    return response

                except Exception as ex:
                    error_message = f"Error processing {auth_url}. Details: {str(ex)}."
                    response = make_response({"error": error_message}, 500)
                    response.set_cookie(
                        "redirect_attempted",
                        "",
                        expires=0,
                        secure=secure,
                        samesite="Strict",
                    )
                    return response
            except Exception as ex_:
                error_msg = "Error: %s", str(ex_)
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @staticmethod
    def get_callback_url():
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("get_callback_url"):
            try:

                # Get the current URL
                current_url = request.url

                # Parse the current URL into components
                url_parts = urlparse(current_url)

                # Split the path into directories
                directories = url_parts.path.split("/")

                # Remove the last directory (i.e., go up one directory)
                directories = directories[:-2]

                # Add 'callback' to the list of directories
                directories.append("cdc_security/callback")

                # Join the directories back into a path
                new_path = "/".join(directories)

                # Azure AD auth will only work on localhost not ip address
                if os.name == "nt":  # 'nt' is the name for Windows in the os module
                    new_path = new_path.replace("127.0.0.1", "localhost")

                # Create a new URL with the new path
                callback_url = urlunparse(
                    (url_parts.scheme, url_parts.netloc, new_path, None, None, None)
                )

                return callback_url

            except Exception as ex_:
                error_msg = "Error: %s", str(ex_)
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

   