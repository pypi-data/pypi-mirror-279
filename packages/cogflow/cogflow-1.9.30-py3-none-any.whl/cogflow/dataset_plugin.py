"""
This module provides functionality related to Dataset upload via plugin.
"""

import io
import os

from urllib.parse import urlparse

import requests
from minio import Minio
from . import plugin_config, PluginManager
from .util import make_post_request


class DatasetMetadata:
    """
    Class used for  metadata of Dataset
    """

    def __init__(self, name, description, source, fmt: str):
        self.name = name
        self.description = description
        self.source = source
        self.format = fmt

    def is_file_path(self):
        """
            method to check if the source of  dataset
            is local file path
        :return: boolean true or false
        """
        return os.path.isfile(self.source)

    def is_external_url(self):
        """
            method to check if source of dataset is
            external url
        :return: boolean true or false
        """
        parsed_url = urlparse(self.source)
        return bool(parsed_url.scheme) and parsed_url.netloc

    def to_dict(self):
        """
        return  object as dictionary
        """
        return {
            "name": self.name,
            "description": self.description,
            "source": self.source,
            "format": self.format,
        }


class DatasetPlugin:
    """
    A class to handle dataset-related operations.
    Attributes:
        None
    """

    def __init__(self):
        """
        Initializes DatasetPlugin with environment variables.
        """
        # Retrieve MinIO connection details from environment variables
        self.minio_endpoint = os.getenv(plugin_config.MINIO_ENDPOINT_URL)
        # Check if the environment variable exists and has a value
        if self.minio_endpoint:
            # Remove the http:// or https:// prefix using string manipulation
            if self.minio_endpoint.startswith(("http://", "https://")):
                # Find the index where the protocol ends
                protocol_end_index = self.minio_endpoint.find("//") + 2
                # Get the remaining part of the URL (without the protocol)
                self.minio_endpoint = self.minio_endpoint[protocol_end_index:]
        else:
            print("MINIO_ENDPOINT_URL environment variable is not set.")
        self.minio_access_key = os.getenv(plugin_config.MINIO_ACCESS_KEY)
        self.minio_secret_key = os.getenv(plugin_config.MINIO_SECRET_ACCESS_KEY)
        self.section = "dataset_plugin"

    def create_minio_client(self):
        """
        Creates a MinIO client object.
        Returns:
            Minio: The MinIO client object.
        """
        # Verify plugin activation
        PluginManager().verify_activation(self.section)
        return Minio(
            self.minio_endpoint,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False,
        )  # Change to True if using HTTPS

    def query_endpoint_and_download_file(self, url, output_file, bucket_name):
        """
        Queries an endpoint and downloads a file from it.
        Args:
            url (str): The URL of the endpoint.
            output_file (str): The name of the output file to save.
        Returns:
            tuple: A tuple containing a boolean indicating success and the file URL if successful.
        """
        # Verify plugin activation
        PluginManager().verify_activation(self.section)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.save_to_minio(response.content, output_file, bucket_name)
                return True
            print(f"Request failed with status code {response.status_code}")
            raise Exception("Request could not be successful due to error")
        except requests.exceptions.RequestException as exp:
            print(f"An error occurred: {exp}")
            raise Exception("Exception occurred during the requested operation")

    def save_to_minio(self, file_content, output_file, bucket_name):
        """
        Saves a file to MinIO.
        Args:
            file_content (bytes): The content of the file to be uploaded.
            output_file (str): The name of the file to be uploaded.
            bucket_name (str): The name of the bucket to upload the file to.
        Returns:
            str: The presigned URL of the uploaded file.
        """
        # Verify plugin activation
        PluginManager().verify_activation(self.section)
        # Initialize MinIO client
        minio_client = self.create_minio_client()
        object_name = output_file
        # Check if the bucket exists, if not, create it
        bucket_exists = minio_client.bucket_exists(bucket_name)
        if not bucket_exists:
            try:
                minio_client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' created successfully.")
            except Exception as exp:
                print(f"Bucket '{bucket_name}' couldnot be created.")
                raise exp
        # Put file to MinIO
        try:
            # Upload content to MinIO bucket
            minio_client.put_object(
                bucket_name,
                object_name,
                io.BytesIO(file_content),
                len(file_content),
            )
            print(
                f"File {output_file} uploaded successfully to MinIO bucket"
                f" {bucket_name} as {object_name}."
            )
            presigned_url = minio_client.presigned_get_object(bucket_name, object_name)
            print(f"Access URL for '{object_name}': {presigned_url}")
            return presigned_url
        except Exception as err:
            print(f"Error uploading file: {err}")
            raise Exception(f"Error uploading file: {err}")

    def delete_from_minio(self, object_name, bucket_name):
        """
        Deletes a file from MinIO.
        Args:
            object_name (str): The name of the object (file) to be deleted.
            bucket_name (str): The name of the bucket containing the file.
        Returns:
            bool: True if the file was successfully deleted, False otherwise.
        """
        # Verify plugin activation
        PluginManager().verify_activation(self.section)
        # Initialize MinIO client
        minio_client = self.create_minio_client()
        try:
            # Check if the object exists
            object_exists = minio_client.stat_object(bucket_name, object_name)
            if object_exists:
                # Delete the object from the bucket
                minio_client.remove_object(bucket_name, object_name)
                print(
                    f"File '{object_name}' deleted successfully from bucket '{bucket_name}'."
                )
                return True
            print(f"File '{object_name}' does not exist in bucket '{bucket_name}'.")
            return False
        except Exception as err:
            print(
                f"Error deleting file '{object_name}' from bucket '{bucket_name}': {err}"
            )
            return False

    def register_dataset(self, details: DatasetMetadata):
        """
        :param details:
        :return:
        """
        try:
            # file_content = self.get_dataset_from_source(details)
            output_file = details.name.replace(
                " ", "_"
            )  # if details.name as space in it
            params = None
            data = None
            files = None
            if details.is_external_url():
                # If the dataset is hosted online
                path = "/dataset/register_by_api"
                data = {
                    "url": details.source,
                    "user_id_val": plugin_config.JUPYTER_USER_ID,
                    "file_name": output_file,
                }
            elif details.is_file_path():
                path = "/dataset"
                params = {
                    "dataset_type": 1,
                    "dataset_source_type": 0,
                    "user_id": plugin_config.JUPYTER_USER_ID,
                    "dataset_name": details.name,
                    "description": details.description,
                }
                files = details.source
            else:
                print("Not a valid source")
                raise Exception("Not a valid source")
            url = os.getenv(plugin_config.API_BASEPATH) + path
            return make_post_request(url=url, data=data, params=params, files=files)
        except Exception as e:
            print(str(e))
            raise e
