"""
This module provides functionality related to Kubeflow Pipelines.
"""
from typing import Optional, Dict, Any

import requests
import os
import time
from datetime import datetime
import kfp
from kfp import dsl
from kserve import (
    KServeClient,
    V1beta1InferenceService,
    V1beta1InferenceServiceSpec,
    V1beta1ModelFormat,
    V1beta1ModelSpec,
    V1beta1PredictorSpec,
    V1beta1SKLearnSpec,
    constants,
    utils,
)
from kubernetes import client
from kubernetes.client import V1ObjectMeta
from kubernetes.client.models import V1EnvVar
from tenacity import retry, wait_exponential, stop_after_attempt
import json
from . import plugin_config, PluginManager
from .util import make_post_request, custom_serializer, is_valid_s3_uri


class CogContainer(kfp.dsl._container_op.Container):
    """
    Subclass of Container to add model access environment variables.
    """

    def __init__(self):
        """
        Initializes the CogContainer class.
        """
        super().__init__(image=None, command=None, args=None)

    def add_model_access(self):
        """
        Adds model access environment variables to the container.

        Returns:
            CogContainer: Container instance with added environment variables.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return (
            self.add_env_variable(
                V1EnvVar(
                    name=plugin_config.TRACKING_URI,
                    value=os.getenv(plugin_config.TRACKING_URI),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=plugin_config.S3_ENDPOINT_URL,
                    value=os.getenv(plugin_config.S3_ENDPOINT_URL),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=plugin_config.ACCESS_KEY_ID,
                    value=os.getenv(plugin_config.ACCESS_KEY_ID),
                )
            )
            .add_env_variable(
                V1EnvVar(
                    name=plugin_config.SECRET_ACCESS_KEY,
                    value=os.getenv(plugin_config.SECRET_ACCESS_KEY),
                )
            )
        )


class KubeflowPlugin:
    """
    Class for defining reusable components.
    """

    def __init__(self, image=None, command=None, args=None):
        """
        Initializes the KubeflowPlugin class.
        """
        self.kfp = kfp
        self.kfp.dsl._container_op.Container.AddModelAccess = (
            CogContainer.add_model_access
        )
        self.kfp.dsl._container_op.ContainerOp.AddModelAccess = (
            CogContainer.add_model_access
        )
        self.config_file_path = os.getenv(plugin_config.COGFLOW_CONFIG_FILE_PATH)
        self.section = "kubeflow_plugin"

    @staticmethod
    def pipeline(name=None, description=None):
        """
        Decorator function to define Kubeflow Pipelines.

        Args:
            name (str, optional): Name of the pipeline. Defaults to None.
            description (str, optional): Description of the pipeline. Defaults to None.

        Returns:
            Callable: Decorator for defining Kubeflow Pipelines.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return dsl.pipeline(name=name, description=description)

    def create_component_from_func(
        self,
        func,
        output_component_file=None,
        base_image=None,
        packages_to_install=None,
    ):
        """
        Create a component from a Python function.

        Args:
            func (Callable): Python function to convert into a component.
            output_component_file (str, optional): Path to save the component YAML file. Defaults
            to None.
            base_image (str, optional): Base Docker image for the component. Defaults to None.
            packages_to_install (List[str], optional): List of additional Python packages
            to install in the component.
            Defaults to None.

        Returns:
            kfp.components.ComponentSpec: Component specification.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        training_var = kfp.components.create_component_from_func(
            func=func,
            output_component_file=output_component_file,
            base_image=base_image,
            packages_to_install=packages_to_install,
        )
        self.kfp.dsl._container_op.ContainerOp.AddModelAccess = (
            CogContainer.add_model_access
        )
        return training_var

    @staticmethod
    def client():
        """
        Get the Kubeflow Pipeline client.

        Returns:
            kfp.Client: Kubeflow Pipeline client instance.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return kfp.Client()

    @staticmethod
    def load_component_from_url(url):
        """
        Load a component from a URL.

        Args:
            url (str): URL to load the component from.

        Returns:
            kfp.components.ComponentSpec: Loaded component specification.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return kfp.components.load_component_from_url(url)

    @staticmethod
    def input_path(label: str):
        """
        Create an InputPath component.

        Args:
            label (str): Label for the input path.

        Returns:
            InputPath: InputPath component instance.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return kfp.components.InputPath(label)

    @staticmethod
    def output_path(label: str):
        """
        Create an OutputPath component.

        Args:
            label (str): Label for the output path.

        Returns:
            OutputPath: OutputPath component instance.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        return kfp.components.OutputPath(label)

    @staticmethod
    def serve_model_v2(model_uri: str, name: str = None):
        """
        Create a kserve instance.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided,
            a default name will be generated.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        namespace = utils.get_default_target_namespace()
        if name is None:
            now = datetime.now()
            v = now.strftime("%d%M")
            name = f"predictor_model{v}"
        isvc_name = name
        predictor = V1beta1PredictorSpec(
            service_account_name="kserve-controller-s3",
            min_replicas=1,
            model=V1beta1ModelSpec(
                model_format=V1beta1ModelFormat(
                    name=plugin_config.ML_TOOL,
                ),
                storage_uri=model_uri,
                protocol_version="v2",
            ),
        )

        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=client.V1ObjectMeta(
                name=isvc_name,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"},
            ),
            spec=V1beta1InferenceServiceSpec(predictor=predictor),
        )
        kserve = KServeClient()
        kserve.create(isvc)
        time.sleep(plugin_config.TIMER_IN_SEC)

    @staticmethod
    def serve_model_v1(model_uri: str, name: str = None):
        """
        Create a kserve instance version1.

        Args:
            model_uri (str): URI of the model.
            name (str, optional): Name of the kserve instance. If not provided,
            a default name will be generated.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        isvc_name = name
        namespace = utils.get_default_target_namespace()
        isvc = V1beta1InferenceService(
            api_version=constants.KSERVE_V1BETA1,
            kind=constants.KSERVE_KIND,
            metadata=V1ObjectMeta(
                name=isvc_name,
                namespace=namespace,
                annotations={"sidecar.istio.io/inject": "false"},
            ),
            spec=V1beta1InferenceServiceSpec(
                predictor=V1beta1PredictorSpec(
                    service_account_name="kserve-controller-s3",
                    sklearn=V1beta1SKLearnSpec(storage_uri=model_uri),
                )
            ),
        )

        kclient = KServeClient()
        kclient.create(isvc)
        time.sleep(plugin_config.TIMER_IN_SEC)

    @staticmethod
    def get_model_url(model_name: str):
        """
        Retrieve the URL of a deployed model.

        Args:
            model_name (str): Name of the deployed model.

        Returns:
            str: URL of the deployed model.
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        kclient = KServeClient()

        @retry(
            wait=wait_exponential(multiplier=2, min=1, max=10),
            stop=stop_after_attempt(30),
            reraise=True,
        )
        def assert_isvc_created(kserve_client, isvc_name):
            """Wait for the Inference Service to be created successfully."""
            assert kserve_client.is_isvc_ready(
                isvc_name
            ), f"Failed to create Inference Service {isvc_name}."

        assert_isvc_created(kclient, model_name)

        isvc_resp = kclient.get(model_name)
        isvc_url = isvc_resp["status"]["address"]["url"]
        return isvc_url

    @staticmethod
    def delete_served_model(model_name: str):
        """
        Delete a deployed model by its ISVC name.

        Args:
            model_name (str): Name of the deployed model.

        Returns:
            None
        """
        # Verify plugin activation
        PluginManager().verify_activation(KubeflowPlugin().section)

        kclient = KServeClient()

        # Attempt to delete the inference service
        response = kclient.delete(model_name)
        if (
            response.get("status", {}).get("conditions", [{}])[0].get("type")
            == "IngressReady"
        ):
            return f"Inference Service {model_name} has been deleted successfully."
        raise Exception(f"Failed to delete Inference Service {model_name}.")


    def get_pipeline_and_experiment_details(run_id):

        try:
            # Get the run details using the run_id
            client = KubeflowPlugin.client()
            run_detail = client.get_run(run_id)
            # Extract run details
            run = run_detail.run
            pipeline_id = run.pipeline_spec.pipeline_id
            experiment_id = run.resource_references[0].key.id
            run_details =  {
                "uuid" : run.id,
                "display_name" : run.name,
                "name" : run.name,
                "description" : run.description,
                "experiment_uuid" : experiment_id,
                "pipeline_uuid" : pipeline_id,
                "createdAt_in_sec" : run.created_at,
                "scheduledAt_in_sec" :run.scheduled_at,
                "finishedAt_in_sec" : run.finished_at,
                "state": run.status
            }

            # Get experiment details using the experiment_id
            experiment = client.get_experiment(experiment_id=experiment_id)

            experiment_details = {
                "uuid" : experiment.id,
                "name" : experiment.name,
                "description" : experiment.description,
                "createdatinSec" : experiment.created_at
            }

            # Get pipeline details using the pipeline_id
            pipeline = client.get_pipeline(pipeline_id=pipeline_id)

            pipeline_details = {
                "uuid":pipeline.id,
                "createdAt_in_sec": pipeline.created_at,
                "name" : pipeline.name,
                "description" : pipeline.description,
                "parameters" : pipeline.parameters,
                "experiment_uuid":experiment.id,
                "pipeline_spec":run.pipeline_spec.workflow_manifest,
                "status": run.status
            }


            workflow_manifest = run_detail.pipeline_runtime.workflow_manifest
            workflow = json.loads(workflow_manifest)

            # Extract the task details
            tasks = workflow['status']['nodes']

            task_details = []
            for task_id, task_info in tasks.items():
                task_detail = {
                    'uuid': task_id,
                    'name': task_info.get('displayName'),
                    'state': task_info.get('phase'),
                    'runuuid': run.id,
                    'startedtimestamp': task_info.get('startedAt'),
                    'finishedtimestamp': task_info.get('finishedAt'),
                    'createdtimestamp' : task_info.get('createdAt')
                }
                task_details.append(task_detail)

            steps = workflow['status']['nodes']
            model_uris = []
            print(steps)
            for step_name, step_info in steps.items():
                if step_info['type'] == 'Pod':
                    outputs = step_info.get('outputs', {}).get('parameters', [])
                    for output in outputs:
                        # print(output)
                        print(f"Artifact: {output['name']}")
                        print(f"URI: {output['value']}")
                        if(is_valid_s3_uri(output['value'])):
                            model_uris.append(output['value'])
                    else:
                        print("Not valid model-uri")
            model_uris = list(set(model_uris))

            model_ids=[]
            for model_uri in model_uris:
                # Define the URL
                url = os.getenv(plugin_config.API_BASEPATH) + "/models/uri"
                data = {
                    "uri": model_uri
                }
                json_data = json.dumps(data)
                headers = {
                    'Content-Type': 'application/json'
                }
                # Make the GET request
                response = requests.get(url,data=json_data,headers= headers)

                # Check if the request was successful
                if response.status_code == 200:
                    # Print the response content
                    # print('Response Content:')
                    model_ids.append(response.json()['data'])
                else:
                    print(f"Failed to retrieve data: {response.status_code}")

            return {
                'run_details': run_details,
                'experiment_details': experiment_details,
                'pipeline_details': pipeline_details,
                'task_details': task_details,
                'model_ids': model_ids
            }
        except Exception as e:
            print(e)


    def save_pipleline_details_to_db(self,details):
        data = json.dumps(details, default=custom_serializer, indent=4)
        url = os.getenv(plugin_config.API_BASEPATH) + "/pipeline/add"
        make_post_request(url=url,data=data)


    def create_run_from_pipeline_func(
            self,
            pipeline_func: ...,
            arguments: Optional[Dict[str, Any]] = None,
            run_name: Optional[str] = None,
            experiment_name: Optional[str] = None,
            namespace: Optional[str] = None,
            pipeline_root: Optional[str] = None,
            enable_caching: Optional[bool] = None,
            service_account: Optional[str] = None,
            experiment_id: Optional[str] = None,
    ):
     run_details = self.client().create_run_from_pipeline_func(pipeline_func,
                                                 arguments,
                                                 run_name,
                                                 experiment_name,
                                                 namespace,
                                                 pipeline_root,
                                                 enable_caching,
                                                 service_account,
                                                 experiment_id)
     # Poll the run status
     poll_interval = 10  # seconds
     while not self.is_run_finished(run_details.run_id):
         status = self.get_run_status(run_details.run_id)
         print(f"Run {run_details.run_id} status: {status}")
         time.sleep(poll_interval)

     details = self.get_pipeline_and_experiment_details(run_details.run_id)
     self.save_pipleline_details_to_db(details)
     return run_details

    def is_run_finished(run_id):
        status = client.get_run(run_id).run.status
        return status in ['Succeeded', 'Failed', 'Skipped', 'Error']

    def get_run_status(run_id):
        return client.get_run(run_id).run.status



