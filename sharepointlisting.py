from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

def list_files_and_metadata(site_url, username, password):
    try:
        # Authenticate with SharePoint
        ctx_auth = AuthenticationContext(url=site_url)
        if ctx_auth.acquire_token_for_user(username, password):
            # Create a client context
            ctx = ClientContext(site_url, ctx_auth)
            
            # Retrieve the list of files from the Documents library
            library = ctx.web.lists.get_by_title("Documents")
            files = library.get_items()
            ctx.load(files)
            ctx.execute_query()
            
            # Iterate through the files and print their metadata
            for file in files:
                file_properties = file.properties
                print("File Properties:", file_properties)
                print()
        else:
            print("Failed to authenticate with SharePoint")
    except Exception as ex:
        print("Error:", ex)


# Example usage
site_url = "https://iotaanalyticscom.sharepoint.com/sites/shivamattooconnectortest"
username = "shiva.mattoo@iotaanalytics.com"
password = "NOqsz756"

list_files_and_metadata(site_url, username, password)
