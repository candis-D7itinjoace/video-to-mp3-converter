import pika, os, sys, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3
import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("initiating the service ....") 
    client = MongoClient("host.minikube.internal", 27017)
    db_videos = client.videos
    db_mp3s = client.mp3s
    logging.info("databases connected")
    # gridfs 
    fs_videos = gridfs.GridFS(db_videos)
    fs_mp3s = gridfs.GridFS(db_mp3s)

    # rabbitmq
    connection = pika.BlockingConnection(
                pika.ConnectionParameters("rabbitmq")
            )
    channel = connection.channel()
    logging.info("connection channel established successfully")
    def callback(ch, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, ch)
        if err:
            logging.warning("error while conversion")
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info("video queued successfully")
    channel.basic_consume(
            queue=os.environ.get("VIDEO_QUEUE"),
            on_message_callback=callback,
        )
    print("waiting for messages..., to exit press ctrl + C ")
    channel.start_consuming()

if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt: 
        print("gracefully shutdown interruption")
        try:
           connection.close()
           client.close()
           sys.exit(0)
        except SystemExit:
            os._exit(0)
