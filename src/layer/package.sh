# This script packages the Python dependencies for the AWS Lambda layer.
# It creates a virtual environment, installs the required packages, and zips the content for deployment.
# Usage: ./package.sh
# Ensure you have Python 3.13 installed and available in your PATH
# Ensure you have the required permissions to execute this script


python3.13 -m venv url_layer
source url_layer/bin/activate
pip install -r requirements.txt

# 
mkdir python
cp -r url_layer/lib python/
zip -r url_layer_content.zip python