import tweepy
from datetime import date
import csv
import os
from google.cloud import storage

def create_csv(tweets):
    file = "/tmp/tweets.csv"
    with open(file, "w", encoding="UTF8") as f:
        header = ["name", "id", "text", "date"]
        today = str(date.today())
        writer = csv.writer(f)
        writer.writerow(header)

        for tweet in tweets:
            name = tweet[0]
            tweet = tweet[1].data

            for t in tweet:
                row = [name, t.id, str(t.text), today]
                writer.writerow(row)

    return file


def save_to_bucket(filename: str):
    storage_client = storage.Client()
    bucket_name = "tweets_datalake"
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename[5:])  # Destination: tweets_datalake/filename
    blob.upload_from_filename(filename)
    print(f"File {filename} uploaded")


def main():

    bearer_token = ""

    api = tweepy.Client(bearer_token=bearer_token)

    topics = ["javier milei", "alberto fernandez", "larreta"]
    tweets = []

    for topic in topics:
        query = f"{topic} -has:links -is:retweet -is:reply -has:media lang:es"
        tweet = api.search_recent_tweets(query=query, max_results=100)
        tweets.append((topic, tweet))

    filename = create_csv(tweets)

    if filename is not None:
        save_to_bucket(filename)
        print("File Saved")
    else:
        print("No file")


if __name__ == "__main__":
    main()
