# Twitter sentiment analysis

## Description

This is a research project with the goal of creating sentiment metrics on the most influential political figures in Argentina. I built an ETL pipeline on the Google Cloud platform that retrieves hundreds of tweets that mention the people of intereset from Twitter's API on a daily basis, and then performs sentiment analysis using Google's natural language API.

The politicians used for this project are:

- Javier Milei: Libertarian, deputy for Buenos Aires
- Larreta: Center-right, mayor of Buenos Aires
- Alberto Fernandez: Center-left, President


## Architecture

![diagram_png](https://user-images.githubusercontent.com/66125885/172054167-ba6eb893-6149-4c08-994a-f72d0e7ff68b.png)


1. Data Extraction is done in airflow using python’s tweepy module on Twitter’s API

2. Transformation: Extracted data is cleaned and each tweet is mapped to the Natural Language API in PySpark with Dataproc

3. Data warehouse: Data is stored in BigQuery, and plotted in Data Studio through its connector


## Results

After collecting samples for a month, I found that:

For Javier Milei, there was a clear negative shift starting from june 10, right after some controversial statements made by him about gun laws and organ trade, which caused his party to break up.

For the other politicians, I found that the sentiment was mixed, with a slightly negative tendency for both of them.


- Live dashboard:

https://datastudio.google.com/reporting/c3898edd-aeab-4872-b64c-00e253958318/page/Ys5xC


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
