
#IoT Device commands
async def iot_download_model(request):
    global log
    log.info("IoT Download Model called")
    response = MethodResponse.create_from_method_request(
        request, status=200
    )
    await device_client.send_method_response(response)  # send response


async def iot_upload_images(request):
    global log
    log.info("IoT Upload Images called")
    response = MethodResponse.create_from_method_request(
        request, status=200
    )
    await device_client.send_method_response(response)  # send response


async def iot_blink(request):
    global log
    log.info("IoT Blink called")
    response = MethodResponse.create_from_method_request(
        request, status=200
    )
    await device_client.send_method_response(response)  # send response
