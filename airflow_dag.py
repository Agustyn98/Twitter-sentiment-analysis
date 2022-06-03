import datetime
import os
from airflow import models
from airflow.operators import python
from scraper import main as scrap_call
from airflow.providers.google.cloud.operators.dataproc import (
    ClusterGenerator,
    DataprocCreateClusterOperator,
    DataprocSubmitPySparkJobOperator,
)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/agus/programas/sentyment_analysys_project/avid-streamer-351318-ddadcd004872.json"

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    "owner": "Agus",
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": datetime.timedelta(minutes=20),
    "start_date": YESTERDAY,
}

with models.DAG(
    "sentyment_analysis_pipeline",
    catchup=False,
    default_args=default_args,
    schedule_interval=datetime.timedelta(hours=24),
) as dag:

    create_csv_operator = python.PythonOperator(task_id="scrap", python_callable=scrap_call)

    path_pip = (
        "gs://goog-dataproc-initialization-actions-us-central1/python/pip-install.sh"
    )
    path_bigquery = (
        "gs://goog-dataproc-initialization-actions-us-central1/connectors/connectors.sh"
    )

    CLUSTER_GENERATOR_CONFIG = ClusterGenerator(
        idle_delete_ttl=300,
        service_account_scopes=["https://www.googleapis.com/auth/cloud-platform"],
        project_id="avid-streamer-351318",
        zone="us-central1-a",
        master_machine_type="n1-standard-2",
        master_disk_size=30,
        num_workers=0,
        init_actions_uris=[path_pip, path_bigquery],
        metadata={
            "PIP_PACKAGES": "google-cloud-language",
            "bigquery-connector-version": "1.2.0",
            "spark-bigquery-connector-version": "0.21.0",
        },
    ).make()

    create_cluster_operator = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        cluster_name="sentyment-analysis-cluster",
        project_id="avid-streamer-351318",
        region="us-central1",
        cluster_config=CLUSTER_GENERATOR_CONFIG,
    )

    submit_job_operator = DataprocSubmitPySparkJobOperator(
        cluster_name="sentyment-analysis-cluster",
        region="us-central1",
        task_id="submit_job",
        main="gs://tweets_datalake1/transformation.py",
    )

    create_csv_operator >> create_cluster_operator >> submit_job_operator

