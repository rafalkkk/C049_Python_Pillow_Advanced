# pip install azure-cognitiveservices-vision-computervision pillow opencv-python

import cv2
import time
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

# Configure connection to Azure 
# copy your own key and edpoint from Azure portal below to KEY and ENDPOINT variables
KEY = "COPY-YOUR-KEY-HERE"
ENDPOINT = "COPY-YOUR-ENDPOINT-HERE"

client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# Send image to Azure Read API
print("Sending image to  Azure AI Vision...")
with open('letter-to-santa-claus.png', "rb") as image_stream:
    # Run OCR (it is asynchronous, so we get an operation ID to check later for results)
    read_operation = client.read_in_stream(image_stream, raw=True)

# Get opertion ID from the response, so we can use it later to check for results
operation_location = read_operation.headers["Operation-Location"]
operation_id = operation_location.split("/")[-1]

# Wait until the opration is completed
while True:
    read_result = client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Display results (or error)
print("\n--- TEXT ---")
if read_result.status == OperationStatusCodes.succeeded:
    for text_result in read_result.analyze_result.read_results:
        for line in text_result.lines:
            print(line.text)