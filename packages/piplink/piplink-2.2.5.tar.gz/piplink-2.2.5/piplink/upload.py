import os
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import hashlib
import re
import getpass

def get_package_info():
    with open("setup.py", "r") as f:
        setup_content = f.read()
    
    def find_match(field_name):
        return re.search(rf"{field_name}\s*=\s*['\"]([^'\"]+)['\"]", setup_content)
    
    name_match = find_match("name")
    version_match = find_match("version")
    description_match = find_match("description")
    author_match = find_match("author")
    author_email_match = find_match("author_email")
    url_match = find_match("url")
    long_description_match = find_match("long_description")
    
    if not name_match or not version_match or not description_match:
        raise ValueError("Package name, version, or description not found in setup.py")
    
    package_info = {
        "name": name_match.group(1),
        "version": version_match.group(1),
        "description": description_match.group(1),
        "author": author_match.group(1) if author_match else "",
        "author_email": author_email_match.group(1) if author_email_match else "",
        "url": url_match.group(1) if url_match else "",
        "long_description": long_description_match.group(1) if long_description_match else ""
    }
    
    return package_info

def main():
    # Prompt for PyPI token (input is hidden)
    token = getpass.getpass("Enter your PyPI token: ").strip()

    # Set the API endpoint for PyPI
    pypi_api = "https://upload.pypi.org/legacy/"

    # Get the package info from setup.py
    try:
        package_info = get_package_info()
    except ValueError as e:
        print(e)
        exit(1)

    # Wait a bit to ensure the file is created (assuming the user has run `python setup.py sdist`)
    time.sleep(5)

    # Get the distribution file path
    dist_file = f"dist/{package_info['name']}-{package_info['version']}.tar.gz"

    # Check if the distribution file exists
    if not os.path.isfile(dist_file):
        print(f"File {dist_file} not found. Make sure the setup.py file ran correctly.")
        exit(1)

    try:
        # Open the distribution file in binary mode
        with open(dist_file, "rb") as f:
            # Calculate the MD5 digest
            md5 = hashlib.md5(f.read()).hexdigest()
            f.seek(0)  # Reset the file pointer

            # Prepare the multipart form data
            encoder = MultipartEncoder(
                fields={
                    ":action": "file_upload",
                    "protocol_version": "1",
                    "name": package_info['name'],
                    "version": package_info['version'],
                    "content": (os.path.basename(dist_file), f, "application/gzip"),
                    "md5_digest": md5,
                    "filetype": "sdist",
                    "metadata_version": "2.1",
                    "description": package_info['description'],
                    "author": package_info['author'],
                    "author_email": package_info['author_email'],
                    "url": package_info['url'],
                    "long_description": package_info['long_description'],
                    "long_description_content_type": "text/markdown",
                    "readme": ("README.md", open("README.md", "rb").read())
                }
            )

            # Set the headers for the API request
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": encoder.content_type
            }

            # Make the API request to upload the package
            response = requests.post(pypi_api, headers=headers, data=encoder.to_string())

            # Check if the upload was successful
            if response.status_code == 200:
                print(f"Package {package_info['name']} {package_info['version']} uploaded successfully!")
                print(f"LinkedIn: https://pypi.org/project/{package_info['name']}/{package_info['version']}")
            else:
                # Extract the error message from the HTML response
                error_message = re.search(r"<h1>(.*?)</h1>", response.text)
                if error_message:
                    print(f"Error uploading package: {response.status_code} {error_message.group(1)}")
                else:
                    print(f"Error uploading package: {response.status_code}")
    except FileNotFoundError:
        print(f"File {dist_file} not found after running sdist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
    
