import datetime
from fileinput import filename
import os
import time
from airflow import models
from airflow.models import Variable
from airflow.operators import python
from scraper import main as scrap_call
from airflow.providers.google.cloud.operators.dataproc import (
    ClusterGenerator,
    DataprocCreateClusterOperator,
    DataprocSubmitPySparkJobOperator,
)


YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    "owner": "Agus",
    "depends_on_past": False,
    "email": [""],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": datetime.timedelta(minutes=20),
    "start_date": YESTERDAY,
}


def set_timestamp_variable():
    Variable.set("filename", '/tmp/tweets-' + str(int(time.time())) + '.csv')


with models.DAG(
    "sentyment_analysis_pipeline",
    catchup=False,
    default_args=default_args,
    schedule_interval=datetime.timedelta(hours=10),
) as dag:


    set_timestamp = python.PythonOperator(task_id="timestamp", python_callable=set_timestamp_variable)

    filename = Variable.get('filename', default_var=0)

    create_csv_operator = python.PythonOperator(task_id="scrap", python_callable=scrap_call, op_args=[filename])

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
        arguments=[filename],
        main="gs://tweets_datalake/transformation.py",
    )

    set_timestamp >> create_csv_operator >> create_cluster_operator >> submit_job_operator

