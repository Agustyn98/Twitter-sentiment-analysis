provider "google" {
  project = "avid-streamer-351318"
  region  = "us-central1"
  zone    = "us-central1-c"
}

resource "google_storage_bucket" "default" {
  name          = "tweets-datalake"
  force_destroy = false
  location      = "US-CENTRAL1"
  storage_class = "STANDARD"
  versioning {
    enabled = false
  }
}

resource "google_bigquery_dataset" "default" {
  dataset_id                  = "twitter"
  location                    = "US-CENTRAL1"
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id = "tweets"
}
