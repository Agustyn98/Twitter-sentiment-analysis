# Twitter sentiment analysis

## Description

This is a research project with the goal of creating sentiment metrics on the most influential political figures in Argentina, Javier Milei, Alberto Fernandez and Larreta. I built an ETL pipeline on the Google Cloud platform that retrieves hundreds of tweets that mention the people of intereset from Twitter's API on a daily basis, and then performs sentiment analysis using Google's natural language API.

## Architecture

![diagram_png](https://user-images.githubusercontent.com/66125885/172054167-ba6eb893-6149-4c08-994a-f72d0e7ff68b.png)


1. Data Extraction is done in airflow using python’s tweepy module on Twitter’s API

2. Transformation: Extracted data is cleaned and each tweet is mapped to the Natural Language API in PySpark with Dataproc

3. Data warehouse: Data is stored in BigQuery, and plotted in Data Studio through its connector


## Results

After collecting samples for a month, I found that:

For Javier Milei, there was a clear negative shift starting from june 10, right after some controversial statements made by him which caused his party to break up.

For the other two politicians, overall, I found that the sentiment was slightly negative overall.


![Sentiment_2022-06-05_11-39-51](https://user-images.githubusercontent.com/66125885/172055967-6d505416-a747-4bb6-a435-5fad174e6ef8.png)


- Live dashboard:

![Screenshot_2022-07-18_16-31-46](https://user-images.githubusercontent.com/66125885/179602644-1dc18428-21ec-4ee8-b512-809524f4de41.png)



## Setup instructions
Requirements:
- Terraform
- Twitter API bearer token
- A GCP service account key with owner permissions

1. Edit your bearer token on `scraper.py`

2. Setup the cloud resources

```
terraform init
```
```
terraform apply
```

Initializing Composer will take around 20 minutes.

3. Upload the `scraper.py` script and `airflow_dag.py` to the Composer's instance DAGs folder in cloud storage



The first DAG run will be run inmediatly
