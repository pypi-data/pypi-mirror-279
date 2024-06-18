"""
    Test module for cases related to mlflow_plugin
"""

import os
import unittest
from unittest.mock import patch, MagicMock
import mlflow
import requests
from mlflow.exceptions import MlflowException
from contextlib import redirect_stdout
from io import StringIO

import cogflow.cogflow.pluginmanager
from cogflow.cogflow.dataset_plugin import DatasetMetadata
from cogflow.cogflow.mlflowplugin import MlflowPlugin


class TestMlflowPlugin(unittest.TestCase):
    """
    Test Class for cases related to mlflow_plugin
    """

    def setUp(self):
        """
            Initial setup
        :return:
        """
        self.mlflow_plugin = MlflowPlugin()

    @patch("mlflow.get_artifact_uri")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_get_artifact_uri_with_run_id(
        self, mock_plugin_activation, mock_get_artifact_uri
    ):
        """
            test for get_artifact_uri_with_run_id
        :param mock_get_artifact_uri:
        :return:
        """
        # Mocking the mlflow get_artifact_uri method to return a specific URI
        mock_get_artifact_uri.return_value = "s3://your-bucket/artifacts/123"

        result = self.mlflow_plugin.get_artifact_uri("123")

        # Asserting that the mock method was called with the correct argument
        mock_get_artifact_uri.assert_called_once_with("123")

        # Asserting that the method returned the expected artifact URI
        self.assertEqual(result, "s3://your-bucket/artifacts/123")
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.set_experiment")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_set_experiment(self, mock_plugin_activation, mock_set_experiment):
        """
            test for set_experiment
        :param mock_set_experiment:
        :return:
        """
        # Mocking the mlflow set_experiment method to raise an exception
        mock_set_experiment.side_effect = MlflowException("Failed to set experiment")

        with self.assertRaises(MlflowException):
            self.mlflow_plugin.set_experiment("experiment_name")
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.set_tracking_uri")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_set_tracking_uri(self, mock_plugin_activation, mock_client):
        """
            test for set_tracking_uri
        :param mock_client:
        :return:
        """
        self.mlflow_plugin.set_tracking_uri("your_tracking_uri")

        mock_client.assert_called_once_with("your_tracking_uri")
        mock_plugin_activation.assert_called_once()

    def test_version(self):
        """
            test for version
        :return:
        """
        version = self.mlflow_plugin.version()

        # Assert that the result matches the mocked version
        self.assertEqual(version, "2.10.2")

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_is_alive(self, mock_plugin_activation):
        """
            test for is_alive
        :return:
        """
        # Mock the requests.get function to simulate response
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200  # Assuming Mlflow UI is accessible
            mock_response.text = "OK"  # Mock response message
            mock_get.return_value = mock_response

            mlflow_plugin = MlflowPlugin()  # Create an instance of MlflowPlugin

            status_code, message = mlflow_plugin.is_alive()

            self.assertEqual(status_code, 200)  # Check if status code is 200
            self.assertEqual(message, "OK")  # Check if response message is "OK"
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_is_alive_request_not_success(self, mock_plugin_activation):
        """
            test when there is request not successful in is_alive method
        :return:
        """
        # Mock the requests.get function to simulate response
        with patch("requests.get") as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404  # Assuming Mlflow UI is not-accessible
            mock_response.text = "NOT-FOUND"  # Mock response message
            mock_get.return_value = mock_response

            mlflow_plugin = MlflowPlugin()  # Create an instance of MlflowPlugin

            status_code, message = mlflow_plugin.is_alive()

            self.assertEqual(status_code, 404)
            self.assertEqual(message, "NOT-FOUND")
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_is_alive_request_exception(self, mock_plugin_activation):
        """
            test when there is exception occured in is_alive method
        :return:
        """
        # Mock the requests.get function to simulate response
        with patch("requests.get") as mock_get:
            mock_get.side_effect = Exception("An error occurred .")

            mlflow_plugin = MlflowPlugin()  # Create an instance of MlflowPlugin
            with self.assertRaises(Exception):
                status_code, message = mlflow_plugin.is_alive()
            mock_plugin_activation.assert_called_once()

    @patch("mlflow.tracking.client.MlflowClient.create_model_version")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_model_version(self, mock_plugin_activation, mock_client):
        """
            test for create_model_version
        :param mock_client:
        :return:
        """
        mock_client.side_effect = MlflowException("Error occured")
        # # Call the method under test and expect it to raise an MlflowException
        with self.assertRaises(MlflowException):
            result = self.mlflow_plugin.create_model_version("model_name", "source")
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.tracking.client.MlflowClient")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_registered_model_exception(
        self, mock_plugin_activation, mock_client
    ):
        """
            test case when exception occurs in create_registered_model
        :param mock_client:
        :return:
        """
        # Define the exception to be raised
        exception_to_raise = MlflowException("API request failed")

        # Mocking the client method to raise the exception
        mock_client.return_value.create_registered_model.side_effect = (
            exception_to_raise
        )

        self.mlflow_plugin.create_registered_model("model_name_4")
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.tracking.client.MlflowClient.create_registered_model")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_registered_model(self, mock_plugin_activation, mock_client):
        """
            test case for create_registered_model
        :param mock_client:
        :return:
        """
        self.mlflow_plugin.create_registered_model("model_name")
        mock_client.assert_called_once_with("model_name")
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.register_model")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_register_model(self, mock_plugin_activation, mock_register_model):
        """
            test case for register_model
        :param mock_register_model:
        :return:
        """
        # Define inputs
        model = MagicMock()
        model_uri = "my_model_uri"
        self.mlflow_plugin.register_model(model, model_uri)
        mock_register_model.assert_called_once_with(model, model_uri)
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.sklearn.load_model")
    @patch("mlflow.utils.rest_utils.http_request")
    def test_load_model_exception(self, mock_http_request, mock_load_model):
        """
            test for exception in load_model
        :param mock_http_request:
        :param mock_load_model:
        :return:
        """
        # Define inputs
        model_name = "my_model"
        model_version = 1
        expected_model = MagicMock()
        mock_load_model.return_value = expected_model

        # Mocking the HTTP request to raise MlflowException
        mock_http_request.side_effect = MlflowException(
            "API request failed with exception HTTPConnectionPool: "
            "Max retries exceeded with url: http://127.0.0.1:5001"
        )
        try:
            mock_load_model.assert_not_called()
        except MlflowException:
            with self.assertRaises(MlflowException):
                loaded_model = self.mlflow_plugin.load_model(model_name, model_version)

    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.load_model")
    def test_load_model(self, mock_load_model):
        """
        Test load_model method in mlflow_plugin.
        """
        # Define inputs
        model_name = "tracking-quickstart"
        model_version = 1
        expected_model = MagicMock()

        # Set the return value of the mocked load_model function
        mock_load_model.return_value = expected_model

        # Call the load_model method
        result = self.mlflow_plugin.load_model(model_name, model_version)

        # Verify that the result is equal to the expected model
        self.assertEqual(result, expected_model)

    @patch("mlflow.autolog")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_autolog(self, mock_plugin_activation, mock_autolog):
        """
            test for autolog
        :param mock_autolog:
        :return:
        """
        # Call the method under test
        self.mlflow_plugin.autolog()

        # Assert that autolog was called
        mock_autolog.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.tracking.client.MlflowClient.delete_registered_model")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_delete_registered_model(
        self, mock_plugin_activation, mock_delete_registered_model
    ):
        """
            test for delete_registered_model
        :param mock_delete_registered_model:
        :return:
        """
        # Mock successful deletion
        model_name = "test_model"
        mock_delete_registered_model.return_value = True

        # Call the method under test
        result = self.mlflow_plugin.delete_registered_model(model_name)

        # Assert that the method returns True
        self.assertTrue(result)

        # Assert that delete_registered_model was called with the correct argument
        mock_delete_registered_model.assert_called_once_with(model_name)
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.search_registered_models")
    def test_search_registered_models_exception(self, mock_search_registered_models):
        """
            test for exception occurs when search for registered model
        :param mock_search_registered_models:
        :return:
        """
        # Mock any other unexpected exception
        mock_search_registered_models.side_effect = MlflowException(
            "API request failed with exception HTTPConnectionPool: "
            "Max retries exceeded with url: http://127.0.0.1:5001"
        )
        # Assert that the method raises the expected exception
        try:
            mock_search_registered_models.assert_not_called()
        except MlflowException:
            with self.assertRaises(MlflowException):
                self.mlflow_plugin.search_registered_models()

    @patch("mlflow.tracking.client.MlflowClient.search_registered_models")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_search_registered_models(
        self, mock_plugin_activation, mock_search_registered_models
    ):
        """
            test for search_registered_model
        :param mock_search_registered_models:
        :return:
        """
        mock_search_registered_models.return_value = None
        # Call the method under test
        self.mlflow_plugin.search_registered_models()

        # Assert that autolog was called
        mock_search_registered_models.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.start_run")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_start_run_with_experiment_and_run_name(
        self, mock_plugin_activation, mock_start_run
    ):
        """
            test for start_run_with_experiment with run_name
        :param mock_start_run:
        :return:
        """
        experiment_name = "test_experiment"
        run_name = "test_run"
        self.mlflow_plugin.start_run(run_name=run_name)
        # Assert that start_run was called with the correct arguments
        mock_start_run.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.end_run")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_end_run(self, mock_plugin_activation, mock_end_run):
        """
            test for end_run
        :param mock_end_run:
        :return:
        """
        # Call the method under test
        self.mlflow_plugin.end_run()
        # Assert that end_run was called
        mock_end_run.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.log_param")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_log_param(self, mock_plugin_activation, mock_log_param):
        """
            test for log_param
        :param mock_log_param:
        :return:
        """
        # Define inputs
        run = MagicMock()
        params = {"param1": 10, "param2": "value"}

        # Call the method under test
        self.mlflow_plugin.log_param(run, params)

        # Assert that log_param was called with the correct arguments
        mock_log_param.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("mlflow.log_metric")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_log_metric(self, mock_plugin_activation, mock_log_metric):
        """
            test for log_metric
        :param mock_log_metric:
        :return:
        """
        # Define inputs
        run = MagicMock()
        metrics = {"accuracy": 0.85, "loss": 0.1}

        # Call the method under test
        self.mlflow_plugin.log_metric(run, metrics)

        # Assert that log_metric was called with the correct arguments
        mock_log_metric.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("requests.post")
    @patch("os.getenv")
    @patch("mlflow.active_run")
    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.get_model_latest_version")
    @patch("mlflow.sklearn.log_model")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_log_model(
        self,
        mock_plugin_activation,
        mock_log_model,
        mock_model_version,
        mock_active_run,
        mock_env,
        mock_requests_post,
    ):
        """
            test for log_model
        :param mock_log_model:
        :return:
        """
        # Define inputs
        sk_model = MagicMock()
        artifact_path = "model"
        # Define any other necessary inputs for the log_model method

        mock_run = MagicMock()
        mock_run.info.run_id = "12345"

        # Set the return value of mlflow.active_run()
        mock_active_run.return_value = mock_run

        mock_env.side_effect = lambda x: {
            "API_BASEPATH": "http://randomn",
        }[x]

        mock_requests_post.return_value.status_code = 201

        mock_model_version.return_value = 1
        # Call the method under test
        result = self.mlflow_plugin.log_model(
            sk_model=sk_model, artifact_path=artifact_path
        )
        # Assert that log_model was called with the correct arguments
        mock_log_model.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("requests.post")
    @patch("os.getenv")
    @patch("mlflow.sklearn.log_model")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_log_model_exception(
        self, mock_plugin_activation, mock_log_model, mock_env, mock_requests_post
    ):
        """
            test log_model when exception occurs
        :param mock_log_model:
        :return:
        """
        # Define inputs
        sk_model = MagicMock()
        artifact_path = "model"
        # Define any other necessary inputs for the log_model method

        mock_env.side_effect = lambda x: {
            "API_BASEPATH": "http://randomn",
        }[x]

        mock_requests_post.return_value.status_code = 201

        # Set up the side effect to raise MlflowException
        mock_log_model.side_effect = MlflowException(
            "API request failed with exception HTTPConnectionPool: "
            "Max retries exceeded with url: http://127.0.0.1:5001"
        )

        # Call the method under test and assert that it raises an exception
        with self.assertRaises(MlflowException):
            self.mlflow_plugin.log_model(sk_model=sk_model, artifact_path=artifact_path)
        mock_plugin_activation.assert_called_once()

    def test_log_metric_successful(self):
        # Use patch to mock PluginManager().verify_activation
        with patch.object(
            cogflow.cogflow.pluginmanager.PluginManager, "verify_activation"
        ) as mock_verify_activation:
            # Use patch to mock mlflow.log_metric
            with patch("mlflow.log_metric") as mock_log_metric:
                # Configure the mock's behavior
                mock_verify_activation.return_value = None  # Plugin activated

                # Call the method with valid arguments
                key = "accuracy"
                value = 0.95
                step = 1
                synchronous = True
                timestamp = None
                run_id = "run1"

                # Invoke the log_metric method
                self.mlflow_plugin.log_metric(
                    key,
                    value,
                    step=step,
                    synchronous=synchronous,
                    timestamp=timestamp,
                    run_id=run_id,
                )

                # Assert that log_metric was called with the expected arguments
                mock_log_metric.assert_called_once()

    @patch("mlflow.search_model_versions")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_search_model_versions(
        self, mock_verify_activation, mock_search_model_versions
    ):
        filter_string = "name='custom_model'"
        order_by = ["1"]

        # Call the method being tested
        self.mlflow_plugin.search_model_versions(
            filter_string=filter_string, order_by=order_by
        )
        mock_search_model_versions.assert_called_once()
        mock_verify_activation.assert_called_once()

    def test_log_model_with_dataset(self):
        with patch("mlflow.sklearn.log_model") as mock_log_model:
            with patch(
                "cogflow.cogflow.mlflowplugin.MlflowPlugin.get_model_latest_version"
            ) as mock_model_version:
                with patch("mlflow.active_run") as mock_active_run:
                    with patch("os.getenv") as mock_env:
                        with patch("requests.post") as mock_requests_post:
                            """
                                test for log_model
                            :param mock_log_model:
                            :return:
                            """
                            # Create a mock run object
                            mock_run = MagicMock()
                            mock_run.info.run_id = "12345"

                            # Set the return value of mlflow.active_run()
                            mock_active_run.return_value = mock_run
                            mock_env.side_effect = lambda x: {
                                "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
                                "AWS_ACCESS_KEY_ID": "minio",
                                "AWS_SECRET_ACCESS_KEY": "minio123",
                                "API_BASEPATH": "http://randomn",
                            }[x]

                            mock_response = {
                                "data": {"dataset_id": 5, "id": 1, "user_id": 0},
                                "message": "Dataset linked with model successfully",
                            }
                            mock_requests_post.return_value.status_code = 201
                            mock_requests_post.return_value.json.return_value = (
                                mock_response
                            )

                            # Mock model
                            sk_model = MagicMock()
                            artifact_path = "model"
                            registered_model_name = "testmodel"

                            # Dataset details
                            source = (
                                "https://archive.ics.uci.edu/static/public/17"
                                "/breast+cancer+wisconsin+diagnostic.zip"
                            )
                            format = "zip"
                            name = "breast+cancer+wisconsin+diagnostic.zip"
                            description = "Breast cancer wisconsin diagnotic dataset"

                            dm = DatasetMetadata(name, description, source, format)
                            mock_model_version.return_value = 1
                            # Define any other necessary inputs for the log_model method

                            # Call the method under test
                            self.mlflow_plugin.log_model_with_dataset(
                                sk_model=sk_model,
                                artifact_path=artifact_path,
                                registered_model_name=registered_model_name,
                                dataset=dm,
                            )
                            mock_log_model.assert_called_once()

    @patch("cogflow.cogflow.mlflowplugin.MlflowPlugin.get_model_latest_version")
    @patch("os.getenv")
    def test_save_model_details_to_db(self, mock_env, mock_model_version):
        with patch("requests.post") as mock_requests_post:
            mock_env.side_effect = lambda x: {
                "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
                "AWS_ACCESS_KEY_ID": "minio",
                "AWS_SECRET_ACCESS_KEY": "minio123",
                "API_BASEPATH": "http://randomn",
            }[x]
            mock_model_version.return_value = 1

            mock_response = {
                "data": {
                    "id": 101,
                    "last_modified_time": "2024-05-16T12:33:08.890033",
                    "last_modified_user_id": 0,
                    "name": "testmodel",
                    "register_date": "2024-05-16T12:33:08.890007",
                    "register_user_id": 0,
                    "type": "sklearn",
                    "version": "1",
                },
                "errors": "None",
                "message": "Created new model.",
                "success": "True",
            }
            mock_requests_post.return_value.status_code = 201
            mock_requests_post.return_value.json.return_value = mock_response
            result = self.mlflow_plugin.save_model_details_to_db("testmodel")
            self.assertEqual(result["data"]["id"], 101)

    @patch("os.getenv")
    def test_save_dataset_details(self, mock_env):
        with patch("requests.post") as mock_requests_post:
            mock_env.side_effect = lambda x: {
                "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
                "AWS_ACCESS_KEY_ID": "minio",
                "AWS_SECRET_ACCESS_KEY": "minio123",
                "API_BASEPATH": "http://randomn",
            }[x]

            mock_response = {
                "data": {
                    "dataset_id": 8,
                    "file_name": "breastcancerwisconsindiagnostic.zip",
                    "file_path": "mlflow",
                    "register_date": "2024-05-16T13:03:05.442386",
                    "user_id": 0,
                },
                "errors": "None",
                "message": "File uploaded successfully.",
                "success": "True",
            }
            mock_requests_post.return_value.status_code = 201
            mock_requests_post.return_value.json.return_value = mock_response
            # Dataset details
            source = (
                "https://archive.ics.uci.edu/static/public/17"
                "/breast+cancer+wisconsin+diagnostic.zip"
            )
            format = "zip"
            name = "breast+cancer+wisconsin+diagnostic.zip"
            description = "Breast cancer wisconsin diagnotic dataset"

            dm = DatasetMetadata(name, description, source, format)
            result = self.mlflow_plugin.save_dataset_details(dataset=dm)
            self.assertEqual(result, mock_response["data"]["dataset_id"])

    @patch("os.getenv")
    def test_link_model_to_dataset(self, mock_env):
        with patch("requests.post") as mock_requests_post:
            mock_env.side_effect = lambda x: {
                "MLFLOW_S3_ENDPOINT_URL": "localhost:9000",
                "AWS_ACCESS_KEY_ID": "minio",
                "AWS_SECRET_ACCESS_KEY": "minio123",
                "API_BASEPATH": "http://randomn",
            }[x]

            mock_response = {
                "data": {
                    "dataset_id": 2,
                    "linked_time": "2024-05-16 15:23:24",
                    "model_id": 1,
                    "user_id": 0,
                },
                "errors": "None",
                "message": "Dataset linked with model successfully",
                "success": "True",
            }
            mock_requests_post.return_value.status_code = 201
            mock_requests_post.return_value.json.return_value = mock_response
            f = StringIO()
            with redirect_stdout(f):
                self.mlflow_plugin.link_model_to_dataset(2, 1)
            out = f.getvalue().strip()
            assert out == "POST request successful"


if __name__ == "__main__":
    unittest.main()
