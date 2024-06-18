
# CogFlow

CogFlow is a versatile framework designed to manage multiple plugins for cognitive and machine learning tasks. It includes several plugins such as `MlflowPlugin`, `KubeflowPlugin`, and `DatasetPlugin`, which can be activated as needed to extend the capabilities of the framework.

## Getting Started

To begin, import cogflow from the CogFlow module:

```python
import cogflow

```

### Explore the Capabilities of `cogflow`

- **List Attributes and Methods**: Understand the `cogflow` module better with:
    ```python
    print(dir(cogflow))
    ```

- **Get Documentation**: For a comprehensive guide on the `cogflow`, use:
    ```python
    help(cogflow)
    ```

## Environment Variables

To maximize the functionality of CogFlow, set the following environment variables:

- **Mlflow Configuration**:
    - `MLFLOW_TRACKING_URI`: The URI of the Mlflow tracking server.
    - `MLFLOW_S3_ENDPOINT_URL`: The endpoint URL for the AWS S3 service.
    - `ACCESS_KEY_ID`: The access key ID for AWS S3 authentication.
    - `SECRET_ACCESS_KEY`: The secret access key for AWS S3 authentication.

- **Machine Learning Database**:
    - `ML_DB_USERNAME`: Username for connecting to the machine learning database.
    - `ML_DB_PASSWORD`: Password for connecting to the machine learning database.
    - `ML_DB_HOST`: Host address for the machine learning database.
    - `ML_DB_PORT`: Port number for the machine learning database.
    - `ML_DB_NAME`: Name of the machine learning database.

- **CogFlow Database**:
    - `COGFLOW_DB_USERNAME`: Username for connecting to the CogFlow database.
    - `COGFLOW_DB_PASSWORD`: Password for connecting to the CogFlow database.
    - `COGFLOW_DB_HOST`: Host address for the CogFlow database.
    - `COGFLOW_DB_PORT`: Port number for the CogFlow database.
    - `COGFLOW_DB_NAME`: Name of the CogFlow database.

- **MinIO Configuration**:
    - `MINIO_ENDPOINT_URL`: The endpoint URL for the MinIO service.
    - `MINIO_ACCESS_KEY`: The access key for MinIO authentication.
    - `MINIO_SECRET_ACCESS_KEY`: The secret access key for MinIO authentication.

---

By setting the environment variables correctly, you can fully utilize the features and functionalities of the CogFlow framework for your cognitive and machine learning tasks.