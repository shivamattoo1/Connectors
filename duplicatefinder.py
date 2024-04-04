from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import hashlib

from docx import Document
import io

# SharePoint site details

site_url = "https://iotaanalyticscom.sharepoint.com/sites/shivamattooconnectortest"
username = "shiva.mattoo@iotaanalytics.com"
password = "NOqsz756"
library_url = "/sites/shivamattooconnectortest/Shared%20Documents"


ctx = ClientContext(site_url).with_credentials(UserCredential(username, password))

# Specify the relative URL to the document library
#library_url = '/sites/yoursite/Shared Documents'

# Function to compute the MD5 hash of a file's content
def compute_file_hash(file):
    stream = file.open_binary_stream()
    ctx.execute_query()
    hasher = hashlib.md5()

    # Directly reading binary data from the stream
    if hasattr(stream, "value") and stream.value:
        # Ensure we're reading the binary content correctly
        binary_content = stream.value
        hasher.update(binary_content)
        return hasher.hexdigest()
    else:
        print(f"Could not read binary content for file: {file.name}")
        return None


# Retrieve files from the document library
library_folder = ctx.web.get_folder_by_server_relative_url(library_url)
files = library_folder.files
ctx.load(files)
ctx.execute_query()

# Verify files are listed
print("Files retrieved from the library:")
for file in files:
    print(file.name)

# Collect file sizes
files_by_size = {}
for file in files:
    # Load properties for each file to ensure size is accessible
    ctx.load(file)
ctx.execute_query()
# The rest of the script remains largely the same.
# The key difference is in how the compute_file_hash function is implemented.

# Ensure you load the file properties before attempting to access them.
for file in files:
    print(f"Hashing file: {file.name}")
    file_hash = compute_file_hash(file)
    print(f"File: {file.name}, Hash: {file_hash}")

# Continue with the size and hash comparison logic as before.

# After identifying files with matching hashes, report them as duplicates.


for file in files:
    if file.length not in files_by_size:
        files_by_size[file.length] = [file]
    else:
        files_by_size[file.length].append(file)

# Detect duplicates based on size and hash
duplicates = []
for size, files_with_same_size in files_by_size.items():
    if len(files_with_same_size) > 1:
        hash_map = {}
        for file in files_with_same_size:
            file_hash = compute_file_hash(file)
            if file_hash in hash_map:
                duplicates.append((hash_map[file_hash], file.name))
            else:
                hash_map[file_hash] = file.name

# Output results
if duplicates:
    print("Duplicate files found based on hash:")
    for dup in duplicates:
        print(f"{dup[0]} and {dup[1]} are duplicates.")
else:
    print("No duplicate files found based on hash.")


def get_docx_files(ctx, library_url):
    """
    List all DOCX files in the specified SharePoint document library.
    """
    library_folder = ctx.web.get_folder_by_server_relative_url(library_url)
    files = library_folder.files
    ctx.load(files)
    ctx.execute_query()
    return [file for file in files if file.name.endswith('.docx')]

def get_file_content(ctx, file):
    """
    Download a file's content from SharePoint.
    """
    response = file.open_binary_stream()
    ctx.execute_query()
    return response.value

def get_docx_text(content):
    """
    Extract text from a DOCX file's binary content.
    """
    doc = Document(io.BytesIO(content))
    full_text = [para.text for para in doc.paragraphs]
    return '\n'.join(full_text)

def compare_docx_contents(content1, content2):
    """
    Compare the text content of two DOCX files.
    """
    text1 = get_docx_text(content1)
    text2 = get_docx_text(content2)
    return text1 == text2

# Fetch all DOCX files from the document library
docx_files = get_docx_files(ctx, library_url)

# Compare each pair of DOCX files to identify duplicates
duplicates = []
for i in range(len(docx_files)):
    content1 = get_file_content(ctx, docx_files[i])
    for j in range(i + 1, len(docx_files)):
        content2 = get_file_content(ctx, docx_files[j])
        if compare_docx_contents(content1, content2):
            duplicates.append((docx_files[i].name, docx_files[j].name))

# Output the results
if duplicates:
    print("Duplicate DOCX files found based on text content:")
    for dup in duplicates:
        print(f"{dup[0]} and {dup[1]} are duplicates.")
else:
    print("No duplicate DOCX files found based on text content.")