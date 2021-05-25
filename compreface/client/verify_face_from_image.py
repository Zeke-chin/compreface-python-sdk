import requests
from compreface.config.api_list import VERIFICATION_API
import os

from requests_toolbelt.multipart.encoder import MultipartEncoder
from compreface.common.typed_dict import AllOptionsDict, check_fields_by_name
from compreface.common.client import ClientRequest


class VerifyFaceFromImageClient(ClientRequest):
    """
        Verify face in image. It uses source and target images for encode and send to CompreFace 
        server with validation by image id.
    """

    def __init__(self, api_key: str, domain: str, port: str):
        super().__init__()
        self.client_url: str = VERIFICATION_API
        self.api_key: str = api_key
        self.url: str = domain + ':' + port + self.client_url

    def get(self):
        pass

    """
        POST request for verify face in image using source and target images. 
        
        :param source_image_path: Path to source image in file system.
        :param target_image_path: Path to target image in file system.
        :param image_id: subject id from previously added image. 
        :param options: dictionary with options for server.
        
        :return: json from server.
    """

    def post(self,
             source_image_path: str = '',
             target_image_path: str = '',
             options: AllOptionsDict = {}) -> dict:

        url: str = self.url + '/verify?'
        source_name_img: str = os.path.basename(source_image_path)
        target_name_img: str = os.path.basename(target_image_path)
        # Validation loop and adding fields to the url.
        for key in options.keys():
            # Checks fields with necessary rules.
            # key - key field by options.
            check_fields_by_name(key, options[key])
            url += '&' + key + "=" + str(options[key])

        # Encoding image from path and encode in multipart for sending to the server.
        m = MultipartEncoder(
            fields={'source_image': (source_name_img, open(
                source_image_path, 'rb')), 'target_image': (target_name_img, open(
                    target_image_path, 'rb'))}

        )

        # Sending encode image for verify face.
        result = requests.post(url, data=m, headers={'Content-Type': m.content_type,
                                                     'x-api-key': self.api_key})
        return result.json()

    def put(self):
        pass

    def delete(self):
        pass
