# Twitter sentiment analysis

## Description

This is a research project with the goal of creating sentiment metrics on the most influential political figures in Argentina. I built an ETL pipeline on the Google Cloud platform that retrieves hundreds of tweets from Twitter's API on a daily basis, and then performs sentiment analysis using Google's natural language API.

## Architecture


1. Data Extraction is done using python’s tweepy module on Twitter’s API

2. Transformation: Data is cleaned and each tweet is mapped to the Natural Language API in PySpark with Dataproc

3. Data is stored in BigQuery, and plotted in Data Studio through its connector


## Results

## Setup instructions
Requirements:
- Terraform
- A GCP account
- A service account key with owner permissions

1. Setup the cloud resources

```
terraform init
```
```
terraform apply
```

Initializing Composer will take around 20 minutes.

2. Upload the `scraper.py` script and `airflow_dag.py` to the Composer's instance DAGs folder in cloud storage



The first DAG run will be run inmediatly
