provider "google" {
  project = "avid-streamer-351318"
  region  = "us-central1"
  zone    = "us-central1-c"
}


resource "google_storage_bucket" "datalake" {
  name          = "tweets_datalake"
  force_destroy = false
  location      = "US-CENTRAL1"
  storage_class = "STANDARD"
  versioning {
    enabled = false
  }
}


resource "google_composer_environment" "airflow" {
  name   = "composer-env1"
  region = "us-central1"

 config {
    software_config {
      image_version = "composer-2-airflow-2"
      pypi_packages = {
        tweepy = ""
      }
    }
  }
}


resource "google_storage_bucket_object" "upload_transformation" {
 name   = "transformation.py"
 source = "PySpark/transformation.py"
 bucket = "tweets_datalake"
  depends_on = [google_storage_bucket.datalake]
}


resource "google_bigquery_dataset" "default_dataset" {
  dataset_id                  = "tweets_datawarehouse"
  location                    = "US-CENTRAL1"
}


resource "google_bigquery_table" "tweets_table" {
  dataset_id = google_bigquery_dataset.default_dataset.dataset_id
  table_id = "tweets"
}
