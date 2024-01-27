import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor



def start(messafe, fs_videos, fs_mp3s, channel):
    json.loads(message)

    # empty temp file creation
    tf = tempfile.NamedTemporaryFile()

    # video content
    out = fs_videos.get(ObjectId(message["video_dif"]))
    
    # add video content to the temp file
    tf.write(out.read())

    # convert the video file to audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()

    #wrtie the audio to a file 
    tf_path = tempfile.gettempdir() + f"/{message["video_fid"]}.mp3"
    audio.write_audiofile(tf_path)

    # save the file to mongo db

    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)
    message["mp3_fid"] = str(fid)

    try:
        channel.basic_publish(
                eschange="",
                routing_key=os.environ.get("MP3_QUEUE"),
                body=json.dumps(message),
                properties=pika.BasicProperties(
                        delivery_mode=pike.spec.PERSISTENT_DELIVERY_MODE
                    ),
            )
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message"
