import os
import unittest
from unittest.mock import patch, MagicMock

from kubernetes.client.models import V1EnvVar

from cogflow.cogflow.kubeflowplugin import KubeflowPlugin, CogContainer
from cogflow.cogflow import plugin_config


class TestKubeflowPlugin(unittest.TestCase):
    def setUp(self):
        self.kfp_plugin = KubeflowPlugin()

    @patch("kfp.dsl.pipeline")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_pipeline_with_name_and_description(
        self, mock_plugin_activation, mock_pipeline
    ):
        self.kfp_plugin.pipeline()
        mock_pipeline.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.create_component_from_func")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_create_component_from_func(
        self, mock_plugin_activation, mock_create_component
    ):
        func = MagicMock()
        self.kfp_plugin.create_component_from_func(func)
        mock_create_component.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.Client")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_client(self, mock_plugin_activation, mock_client):
        # Arrange
        self.kfp_plugin.client()

        # Assertion
        mock_client.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.load_component_from_url")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_load_component_from_url_success(
        self, mock_plugin_activation, mock_load_component
    ):
        # Mock a successful component loading
        expected_component_spec = MagicMock()
        mock_load_component.return_value = expected_component_spec

        # Define a sample URL
        url = "http://example.com/component.tar.gz"

        # Call the function under test
        result = self.kfp_plugin.load_component_from_url(url)

        # Assert that the function returns the expected component specification
        self.assertEqual(result, expected_component_spec)

        # Assert that load_component_from_url was called with the correct URL
        mock_load_component.assert_called_once_with(url)
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.InputPath")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_input_path(self, mock_plugin_activation, mock_input):
        # Define a sample label for the input path
        label = "input_data"

        input_path = self.kfp_plugin.input_path(label)
        mock_input.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch("kfp.components.OutputPath")
    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_output_path(self, mock_plugin_activation, mock_output):
        # Define a sample label for the input path
        label = "output_data"

        input_path = self.kfp_plugin.output_path(label)
        mock_output.assert_called_once()
        mock_plugin_activation.assert_called_once()

    @patch.dict(
        os.environ,
        {
            plugin_config.TRACKING_URI: "tracking_uri_value",
            plugin_config.S3_ENDPOINT_URL: "s3_endpoint_url_value",
            plugin_config.ACCESS_KEY_ID: "access_key_id_value",
            plugin_config.SECRET_ACCESS_KEY: "secret_access_key_value",
        },
    )
    def test_add_model_access(self):
        # Create an instance of CogContainer
        container = CogContainer()

        # Call the AddModelAccess method
        container_with_env_vars = container.add_model_access()

        # Assert that the returned value is an instance of CogContainer
        self.assertIsInstance(container_with_env_vars, CogContainer)

        # Assert that the environment variables are added correctly
        expected_env_vars = [
            V1EnvVar(name=plugin_config.TRACKING_URI, value="tracking_uri_value"),
            V1EnvVar(name=plugin_config.S3_ENDPOINT_URL, value="s3_endpoint_url_value"),
            V1EnvVar(name=plugin_config.ACCESS_KEY_ID, value="access_key_id_value"),
            V1EnvVar(
                name=plugin_config.SECRET_ACCESS_KEY, value="secret_access_key_value"
            ),
        ]

        for expected_env_var in expected_env_vars:
            self.assertIn(expected_env_var, container_with_env_vars.env)

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v2(self, mock_plugin_activation):
        # Patch Kubernetes client to avoid loading kube config
        with patch("kubernetes.config.load_kube_config"):
            model_uri = "sample_model_uri"
            name = "test_model_name"

            # Call the function and assert that it raises MaxRetryError
            with self.assertRaises(Exception):
                self.kfp_plugin.serve_model_v2(model_uri, name)
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v2_no_name(self, mock_plugin_activation):
        with patch("kubernetes.config.load_kube_config"):
            model_uri = "sample_model_uri"

            # Call the function and assert that it raises MaxRetryError
            with self.assertRaises(Exception):
                self.kfp_plugin.serve_model_v2(model_uri)
            mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_serve_model_v1_with_exception(self, mock_plugin_activation):
        # Define input parameters
        model_uri = "example_model_uri"
        name = "test_model_name"

        # Call the function and assert that it raises MaxRetryError
        with self.assertRaises(Exception):
            self.kfp_plugin.serve_model_v1(model_uri, name)
        mock_plugin_activation.assert_called_once()

    @patch("cogflow.cogflow.pluginmanager.PluginManager.verify_activation")
    def test_get_model_url(self, mock_plugin_activation):
        model_name = "test_model"

        with self.assertRaises(Exception):
            # Call the method you're testing here
            self.kfp_plugin.get_model_url(model_name)
        mock_plugin_activation.assert_called_once()


if __name__ == "__main__":
    unittest.main()
