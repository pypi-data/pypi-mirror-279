import logging
import os
from azure.storage.blob import BlobServiceClient, ContentSettings


class BlobUploader:
    def __init__(self, connect_str, container_name, file_name):
        self.filename = file_name
        self.blob_client = BlobServiceClient.from_connection_string(
            connect_str).get_blob_client(container_name, file_name)

    def __upload_blob(self, file_path):
        with open(file_path, "rb") as data:
            content_settings = ContentSettings(content_type="image/png")
            self.blob_client.upload_blob(
                data, blob_type="BlockBlob", content_settings=content_settings)
            logging.warning("Saving image...")
        return True

    def upload_file_to_blob(self):
        try:
            current_dir_image = os.getcwd()
            image_path = os.path.join(current_dir_image, self.filename)
            self.__upload_blob(image_path)
            logging.warning(f" Saving to blob with success")
            return True
        except Exception as e:
            logging.error(f"Error: {e}")
            logging.error(f"Error Description: {str(e)}")
            return
