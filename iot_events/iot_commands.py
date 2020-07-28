from azure.iot.device import MethodResponse
from azure.storage.blob import ContainerClient

import os, logging, app_logger
log:logging.Logger = app_logger.get_logger()

#IoT Device commands
async def iot_download_model(request, device_client, credentials):
    global log
    log.info("IoT Download Model called")
    response = MethodResponse.create_from_method_request(request, status=200)
    await device_client.send_method_response(response)  # send response

    # Setup blob service and container client for downloading from the blob storage
    container = ContainerClient.from_container_url(credentials.tf_models)

    blob_list = container.list_blobs()
    for blob in blob_list:
        if blob.name.endswith(".tflite") or blob.name == "signature.json":
            download_path = os.path.join('./tf_models_lite', blob.name)
            log.info("Downloading %s to %s" % (blob.name, download_path))

            blob_client = container.get_blob_client(blob)
            with open(download_path, "wb") as local_file:
                download_stream = blob_client.download_blob()
                local_file.write(download_stream.readall())
        else:
            pass

async def iot_upload_images(request, device_client, credentials):
    global log
    log.info("IoT Upload Images called")
    response = MethodResponse.create_from_method_request(request, status=200)
    await device_client.send_method_response(response)  # send response

    # Setup blob service and container client for downloading from the blob storage
    container = ContainerClient.from_container_url(credentials.blob_token)

    for filename in os.listdir('img'):
        filepath = 'img/' + filename
        if filename.endswith('.jpg'):
            blob = container.get_blob_client(filename)

            # Upload content to block blob
            with open(filepath, "rb") as data:
                log.info("Uploading %s to blob storage" % (filename))
                blob.upload_blob(data, blob_type="BlockBlob")
            
            # Delete the file once it was uploaded
            if os.path.exists(filepath):
                os.remove(filepath)


async def iot_blink(request, device_client, credentials):
    global log
    log.info("IoT Blink called")
    response = MethodResponse.create_from_method_request(request, status=200)
    await device_client.send_method_response(response)  # send response
