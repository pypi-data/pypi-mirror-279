import logging

from django.http import JsonResponse
from django.views import View

from findmydevice.json_utils import parse_json
from findmydevice.models import Device
from findmydevice.services.device import get_device_by_token


logger = logging.getLogger(__name__)


class KeyView(View):
    """
    /key
    """

    def put(self, request):
        """
        The WebPage/Client requests the private key.
        """
        put_data = parse_json(request)
        access_token = put_data['IDT']

        index = put_data.get('Data')
        if index != 'unused':
            logger.warning('Get private key with Data!="unused" ... Data is: %r', index)

        device: Device = get_device_by_token(token=access_token)
        privkey = device.privkey

        response_data = {'Data': privkey}
        logger.info('PUT key: %r', response_data)
        return JsonResponse(response_data)
