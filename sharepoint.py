from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File

def list_files_and_metadata(site_url, username, password, folder_url):
    try:
        # Authenticate with SharePoint
        ctx_auth = AuthenticationContext(url=site_url)
        if ctx_auth.acquire_token_for_user(username, password):
            # Create a client context
            ctx = ClientContext(site_url, ctx_auth)
            
            # Retrieve the folder by URL
            folder = ctx.web.get_folder_by_server_relative_url(folder_url)
            ctx.load(folder)
            ctx.execute_query()
            
            # Retrieve all files from the folder
            files = folder.files
            ctx.load(files)
            ctx.execute_query()
            
            # Iterate through the files and print their metadata
            for file in files:
                file_properties = file.properties
                print("File Name:", file_properties["Name"])
                print("File URL:", file_properties["ServerRelativeUrl"])
                print("File Size:", file_properties["Length"])
                print("File Created:", file_properties["TimeCreated"])
                print("File Modified:", file_properties["TimeLastModified"])
                print()
        else:
            print("Failed to authenticate with SharePoint")
    except Exception as ex:
        print("Error:", ex)

site_url = "https://iotaanalyticscom.sharepoint.com/sites/shivamattooconnectortest"
username = "shiva.mattoo@iotaanalytics.com"
password = "NOqsz756"
folder_url = "/sites/shivamattooconnectortest/Shared%20Documents"

list_files_and_metadata(site_url, username, password, folder_url)
