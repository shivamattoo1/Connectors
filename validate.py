from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.runtime.client_request_exception import ClientRequestException

def validate_sharepoint_url(site_url, username, password, relative_url):
    try:
        # Authenticate with SharePoint
        ctx_auth = AuthenticationContext(url=site_url)
        if ctx_auth.acquire_token_for_user(username, password):
            # Create a client context
            ctx = ClientContext(site_url, ctx_auth)
            
            # Make the request to validate the server-relative URL
            file = ctx.web.get_file_by_server_relative_url(relative_url)
            ctx.load(file)
            ctx.execute_query()
            
            # If no exception is raised, the URL is valid
            print("Server-relative URL is valid")
        else:
            print("Failed to authenticate with SharePoint")
    except ClientRequestException as ex:
        print("Error:", ex)

# Example usage
site_url = "https://iotaanalyticscom.sharepoint.com/sites/shivamattooconnectortest"
username = "shiva.mattoo@iotaanalytics.com"
password = "NOqsz756"
relative_url = "/sites/shivamattooconnectortest/Shared%20Documents/Forms/AllItems.aspx"  

validate_sharepoint_url(site_url, username, password, relative_url)






