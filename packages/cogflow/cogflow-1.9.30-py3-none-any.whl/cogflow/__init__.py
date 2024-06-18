"""
This module provides configurations, utilities, and management for the CogFlow plugins.

Attributes:
    TRACKING_URI (str): The URI for tracking experiments in the machine learning tool.
    TIMER_IN_SEC (int): Timer interval in seconds, used for scheduling tasks or operations.
    ML_TOOL (str): The machine learning tool being used (e.g., "mlflow").
    ACCESS_KEY_ID (str): Access key ID for authentication, typically for AWS services.
    SECRET_ACCESS_KEY (str): Secret access key for authentication, typically for AWS services.
    S3_ENDPOINT_URL (str): Endpoint URL for connecting to Amazon S3.

    ML_DB_USERNAME (str): Username for connecting to the machine learning database.
    ML_DB_PASSWORD (str): Password for connecting to the machine learning database.
    ML_DB_HOST (str): Host address for the machine learning database.
    ML_DB_PORT (str): Port number for the machine learning database.
    ML_DB_NAME (str): Name of the machine learning database.

    COGFLOW_DB_USERNAME (str): Username for connecting to the CogFlow database.
    COGFLOW_DB_PASSWORD (str): Password for connecting to the CogFlow database.
    COGFLOW_DB_HOST (str): Host address for the CogFlow database.
    COGFLOW_DB_PORT (str): Port number for the CogFlow database.
    COGFLOW_DB_NAME (str): Name of the CogFlow database.

    MINIO_ENDPOINT_URL (str): Endpoint URL for connecting to the MinIO service.
    MINIO_ACCESS_KEY (str): Access key for authentication with MinIO.
    MINIO_SECRET_ACCESS_KEY (str): Secret access key for authentication with MinIO.

Imports:
    plugin_status: Contains plugin status information and management utilities.
    PluginErrors: Defines custom exceptions for handling plugin-related errors.
    PluginManager: Provides the PluginManager class for managing CogFlow plugins.

Usage:
    This module serves as a central configuration hub for the CogFlow framework,
    allowing easy access to settings and utilities for managing plugins and their
    dependencies. The module also includes error handling and plugin status management.
"""

from .plugin_config import (
    TRACKING_URI,
    TIMER_IN_SEC,
    ML_TOOL,
    ACCESS_KEY_ID,
    SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    ML_DB_USERNAME,
    ML_DB_PASSWORD,
    ML_DB_HOST,
    ML_DB_PORT,
    ML_DB_NAME,
    COGFLOW_DB_USERNAME,
    COGFLOW_DB_PASSWORD,
    COGFLOW_DB_HOST,
    COGFLOW_DB_PORT,
    COGFLOW_DB_NAME,
    MINIO_ENDPOINT_URL,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_ACCESS_KEY,
    API_BASEPATH,
)


from .pluginmanager import PluginManager
from .dataset_plugin import DatasetPlugin
from .kubeflowplugin import CogContainer, KubeflowPlugin
from .mlflowplugin import MlflowPlugin


delete_registered_model = MlflowPlugin().delete_registered_model
search_registered_models = MlflowPlugin().search_registered_models
load_model = MlflowPlugin().load_model
register_model = MlflowPlugin().register_model
autolog = MlflowPlugin().autolog
create_registered_model = MlflowPlugin().create_registered_model
create_model_version = MlflowPlugin().create_model_version
set_tracking_uri = MlflowPlugin().set_tracking_uri
set_experiment = MlflowPlugin().set_experiment
get_artifact_uri = MlflowPlugin().get_artifact_uri
start_run = MlflowPlugin().start_run
end_run = MlflowPlugin().end_run
log_param = MlflowPlugin().log_param
log_metric = MlflowPlugin().log_metric
log_model = MlflowPlugin().log_model
pyfunc = MlflowPlugin().pyfunc
mlflow = MlflowPlugin().mlflow
sklearn = MlflowPlugin().sklearn
cogclient = MlflowPlugin().cogclient
tensorflow = MlflowPlugin().tensorflow
pytorch = MlflowPlugin().pytorch
models = MlflowPlugin().models
search_model_versions = MlflowPlugin().search_model_versions


add_model_access = CogContainer().add_model_access
pipeline = KubeflowPlugin().pipeline
create_component_from_func = KubeflowPlugin().create_component_from_func
delete_served_model = KubeflowPlugin().delete_served_model
client = KubeflowPlugin().client
load_component_from_url = KubeflowPlugin().load_component_from_url
input_path = KubeflowPlugin().input_path
output_path = KubeflowPlugin().output_path
serve_model_v2 = KubeflowPlugin().serve_model_v2
serve_model_v1 = KubeflowPlugin().serve_model_v1
get_model_url = KubeflowPlugin().get_model_url
kfp = KubeflowPlugin().kfp


create_minio_client = DatasetPlugin().create_minio_client
query_endpoint_and_download_file = DatasetPlugin().query_endpoint_and_download_file
save_to_minio = DatasetPlugin().save_to_minio
delete_from_minio = DatasetPlugin().delete_from_minio

__all__ = [
    # Methods from MlflowPlugin class
    "delete_registered_model",
    "search_registered_models",
    "load_model",
    "register_model",
    "autolog",
    "create_registered_model",
    "create_model_version",
    "set_tracking_uri",
    "set_experiment",
    "get_artifact_uri",
    "start_run",
    "end_run",
    "log_param",
    "log_metric",
    "log_model",
    "pyfunc",
    "mlflow",
    "sklearn",
    "cogclient",
    "tensorflow",
    "pytorch",
    "models",
    # Method from CogContainer class
    "add_model_access",
    # Methods from KubeflowPlugin class
    "pipeline",
    "create_component_from_func",
    "delete_served_model",
    "client",
    "load_component_from_url",
    "input_path",
    "output_path",
    "serve_model_v2",
    "serve_model_v1",
    "get_model_url",
    "kfp",
    # Methods from DatasetPlugin class
    "create_minio_client",
    "query_endpoint_and_download_file",
    "save_to_minio",
    "delete_from_minio",
]
