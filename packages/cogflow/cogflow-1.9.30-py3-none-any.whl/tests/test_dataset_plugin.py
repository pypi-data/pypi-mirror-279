import unittest
from unittest.mock import patch, MagicMock

import minio
import requests

from cogflow.cogflow.dataset_plugin import DatasetPlugin


class TestDatasetPlugin(unittest.TestCase):
    @patch("requests.get")
    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.save_to_minio")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_query_endpoint_and_download_file_success(
        self, mock_plugin_activation, mock_save_to_minio, mock_requests_get
    ):
        # Arrange
        url = "http://dataset.com/dataset"
        output_file = "dataset.csv"
        bucket_name = "mlpipeline"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test dataset content"
        mock_requests_get.return_value = mock_response

        mock_minio_instance = MagicMock()
        mock_save_to_minio.return_value = "http://dataset.com/dataset.csv"

        # Act
        success = DatasetPlugin().query_endpoint_and_download_file(
            url=url, output_file=output_file, bucket_name=bucket_name
        )

        # Assert
        self.assertTrue(success)
        mock_save_to_minio.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("requests.get")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_query_endpoint_and_download_file_failure(
        self, mock_plugin_activation, mock_requests_get
    ):
        # Arrange
        dataset_plugin = DatasetPlugin()
        url = "http://dataset.com/dataset"
        bucket_name = "mlpipeline"
        output_file = "dataset.csv"
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        # Act & Assert
        with self.assertRaises(Exception):
            dataset_plugin.query_endpoint_and_download_file(
                url, output_file, bucket_name
            )
        mock_plugin_activation.assert_called_once()

    @patch("requests.get")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_request_exception_query_endpoint(
        self, mock_plugin_activation, mock_requests_get
    ):
        # Arrange
        dataset_plugin = DatasetPlugin()
        url = "http://dataset.com/dataset"
        bucket_name = "mlpipeline"
        output_file = "dataset.csv"
        # mock_response = MagicMock()
        # mock_response.status_code = 404
        # mock_requests_get.return_value = mock_response
        mock_requests_get.side_effect = requests.exceptions.RequestException(
            "Request failed"
        )
        with self.assertRaises(Exception):
            dataset_plugin.query_endpoint_and_download_file(
                url, output_file, bucket_name
            )
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("os.getenv")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_save_to_minio_success(
        self, mock_plugin_activation, mock_getenv, mock_create_minio_client
    ):

        # Arrange
        mock_minio_client = MagicMock()
        mock_create_minio_client.return_value = mock_minio_client
        mock_getenv.side_effect = lambda x: {
            "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
        }[x]

        dataset_plugin = DatasetPlugin()
        file_content = b"Test dataset content"
        output_file = "dataset.csv"

        mock_minio_instance = MagicMock()
        mock_minio_instance.bucket_exists.return_value = True
        mock_minio_instance.presigned_get_object.return_value = (
            "http://dataset.com/dataset.csv"
        )

        # Act
        dataset_plugin.save_to_minio(
            file_content, output_file, bucket_name="mlpipeline"
        )
        # Assertions
        mock_minio_client.bucket_exists.assert_called_once_with("mlpipeline")
        mock_minio_client.presigned_get_object.assert_called_once()
        mock_minio_client.put_object.assert_called_once()
        mock_create_minio_client.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("os.getenv")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_minio_bucket_creation(
        self,
        mock_plugin_activation,
        mock_getenv,
        mock_create_minio_client,
    ):
        # Arrange
        mock_minio_client = MagicMock()
        mock_create_minio_client.return_value = mock_minio_client
        mock_getenv.side_effect = lambda x: {
            "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
        }[x]

        dataset_plugin = DatasetPlugin()
        file_content = b"Test dataset content"
        output_file = "dataset.csv"

        mock_minio_client.bucket_exists.return_value = False
        dataset_plugin.save_to_minio(
            file_content, output_file, bucket_name="bucket_name"
        )
        mock_minio_client.make_bucket.assert_called_once()
        mock_minio_client.make_bucket.assert_called_once_with("bucket_name")
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("os.getenv")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_minio_bucket_creation_exception(
        self,
        mock_plugin_activation,
        mock_getenv,
        mock_create_minio_client,
    ):
        # Arrange
        mock_minio_client = MagicMock()
        mock_create_minio_client.return_value = mock_minio_client
        mock_getenv.side_effect = lambda x: {
            "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
        }[x]

        dataset_plugin = DatasetPlugin()
        file_content = b"Test dataset content"
        output_file = "dataset.csv"

        mock_minio_client.bucket_exists.return_value = False
        mock_minio_client.make_bucket.side_effect = Exception(
            "Bucket Cannot be created"
        )
        with self.assertRaises(Exception):
            dataset_plugin.save_to_minio(
                file_content, output_file, bucket_name="bucket_name"
            )
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("os.getenv")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_save_to_exception(
        self, mock_plugin_activation, mock_getenv, mock_create_minio_client
    ):
        # Arrange
        mock_minio_client = MagicMock()
        mock_create_minio_client.return_value = mock_minio_client
        mock_getenv.side_effect = lambda x: {
            "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
        }[x]

        dataset_plugin = DatasetPlugin()
        file_content = b"Test dataset content"
        output_file = "dataset.csv"

        # mock_minio_client.bucket_exists.return_value = False
        # mock_minio_client.make_bucket.side_effect = Exception("Bucket Cannot be created")
        mock_minio_client.put_object.side_effect = Exception(
            "Error while storing object"
        )
        with self.assertRaises(Exception):
            dataset_plugin.save_to_minio(
                file_content, output_file, bucket_name="bucket_name"
            )
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_delete_from_minio_success(
        self, mock_plugin_activation, mock_create_minio_client
    ):
        # Arrange
        dataset_plugin = DatasetPlugin()
        object_name = "test_object"
        bucket_name = "test_bucket"

        mock_minio_instance = MagicMock()
        mock_create_minio_client.return_value = mock_minio_instance
        mock_minio_instance.stat_object.return_value = True  # Object exists

        # Act
        result = dataset_plugin.delete_from_minio(object_name, bucket_name)

        # Assert
        self.assertTrue(result)
        mock_minio_instance.remove_object.assert_called_once_with(
            bucket_name, object_name
        )
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_delete_from_minio_object_not_found(
        self, mock_plugin_activation, mock_create_minio_client
    ):
        # Arrange
        dataset_plugin = DatasetPlugin()
        object_name = "test_object"
        bucket_name = "test_bucket"

        mock_minio_instance = MagicMock()
        mock_create_minio_client.return_value = mock_minio_instance
        mock_minio_instance.stat_object.return_value = False  # Object does not exist

        # Act
        result = dataset_plugin.delete_from_minio(object_name, bucket_name)

        # Assert
        self.assertFalse(result)
        mock_minio_instance.remove_object.assert_not_called()
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.dataset_plugin.DatasetPlugin.create_minio_client")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_delete_from_minio_exception(
        self, mock_plugin_activation, mock_create_minio_client
    ):
        # Arrange
        dataset_plugin = DatasetPlugin()
        object_name = "test_object"
        bucket_name = "test_bucket"

        mock_minio_instance = MagicMock()
        mock_create_minio_client.return_value = mock_minio_instance
        mock_minio_instance.stat_object.side_effect = Exception("Test error")

        # Act
        result = dataset_plugin.delete_from_minio(object_name, bucket_name)

        # Assert
        self.assertFalse(result)
        mock_minio_instance.remove_object.assert_not_called()
        mock_plugin_activation.assert_called_once()

    @patch("os.getenv")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_minio_client(self, mock_plugin_activation, mock_getenv):
        # Define test parameters
        mock_getenv.side_effect = lambda x: {
            "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
            "AWS_ACCESS_KEY_ID": "minio",
            "AWS_SECRET_ACCESS_KEY": "minio123",
        }[x]

        # Create the MinioClient object
        dataset_plugin = DatasetPlugin()
        minio_client = dataset_plugin.create_minio_client()

        # Assert that the MinioClient object is created correctly
        self.assertIsInstance(minio_client, minio.api.Minio)
        mock_plugin_activation.assert_called_once()


if __name__ == "__main__":
    unittest.main()
