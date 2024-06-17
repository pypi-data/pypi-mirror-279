"""
This module provides functionality related to Model actions via plugin.
"""

import os
from .. import plugin_config
from ..pluginmanager import PluginManager
from ..util import make_post_request
from .mlflowplugin import MlflowPlugin


class NotebookPlugin:
    """
    Class for defining reusable components.
    """

    def __init__(self):
        """
        Initializes the ModelPlugin class.
        """
        self.section = "notebook_plugin"

    @staticmethod
    def link_model_to_dataset(dataset_id, model_id):
        """
        Links a model to a dataset using the provided API endpoint.

        This method sends a POST request to the API to associate a specified model
        with a given dataset. It uses the user's ID defined in the plugin configuration.

        Args:
            dataset_id (str): The ID of the dataset to link to the model.
            model_id (str): The ID of the model to be linked to the dataset.

        Returns:
            Response: The response object from the API call.

        Raises:
            requests.exceptions.RequestException: An error occurred when making the POST request.
        """
        # Verify plugin activation
        PluginManager().verify_activation(NotebookPlugin().section)

        data = {
            "user_id": plugin_config.JUPYTER_USER_ID,
            "model_id": model_id,
            "dataset_id": dataset_id,
        }
        # call the api
        url = os.getenv(plugin_config.API_BASEPATH) + "/link_dataset_model"
        return make_post_request(url, data=data)

    def save_model_details_to_db(self, registered_model_name):
        """
        store model details in database
        :param registered_model_name: name of the registered model
        :return: id of model
        """
        # Verify plugin activation
        PluginManager().verify_activation(NotebookPlugin().section)

        data = {
            "name": registered_model_name,
            "version": self.get_model_latest_version(registered_model_name),
            "type": "sklearn",
            "user_id": plugin_config.JUPYTER_USER_ID,
        }

        # call the api to register model
        url = os.getenv(plugin_config.API_BASEPATH) + "/models"
        return make_post_request(url, data=data)

    @staticmethod
    def get_model_latest_version(registered_model_name: str):
        """
        return the latest version of registered model
        :param registered_model_name: model name to get the versions
        :return: latest version
        """
        # Verify plugin activation
        PluginManager().verify_activation(NotebookPlugin().section)

        latest_version_info = MlflowPlugin().search_model_versions(
            filter_string=f"name='{registered_model_name}'"
        )
        sorted_model_versions = sorted(
            latest_version_info, key=lambda x: x.version, reverse=True
        )

        if sorted_model_versions:
            latest_version = sorted_model_versions[0]
            print("Latest Version:", latest_version.version)
            print("Status:", latest_version.status)
            print("Stage:", latest_version.current_stage)
            print("Description:", latest_version.description)
            print("Last Updated:", latest_version.last_updated_timestamp)
            return latest_version.version

        print(f"No model versions found for {registered_model_name}")
        return 1

    @staticmethod
    def save_model_uri_to_db(model_id, model_uri):
        """
            method to call the api to save model uri
        :param model_id: model id of the model
        :param model_uri: model uri
        :return: API response
        """
        # Verify plugin activation
        PluginManager().verify_activation(NotebookPlugin().section)

        # call the api for saving model_uri
        data = {
            "user_id": plugin_config.JUPYTER_USER_ID,
            "model_id": model_id,
            "uri": model_uri,
            "description": f"model uri of model id :{model_id}",
        }
        url = os.getenv(plugin_config.API_BASEPATH) + "/model/uri"
        return make_post_request(url, data=data)
