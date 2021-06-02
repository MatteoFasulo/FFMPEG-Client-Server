import os
import subprocess
import configparser

########################## STATIC INT #############################
HOME = "/home/ubuntu/RC/"
SEP = "<SEPARATOR>"
encoding = 'utf-8'


###################################################################

def streaming(user, filename):
    print("\t Streaming started")
    cfg = configparser.ConfigParser()
    cfg_path = ("{}received{}{}{}{}".format(HOME, os.sep, user, os.sep, "user_config.cfg"))
    cfg.read(cfg_path, encoding="UTF-8")

    source = ("{}encoded{}{}{}{}".format(HOME, os.sep, user, os.sep, filename))

    youtube_url = cfg["FFMPEG"]["youtube_url"]
    youtube_key = cfg["FFMPEG"]["youtube_key"]
    twitch_url = cfg["FFMPEG"]["twitch_url"]
    twitch_key = cfg["FFMPEG"]["twitch_key"]
    debug = cfg["FFMPEG"]["debug"]

    streams = f"[f=flv:onfail=ignore]{twitch_url}{twitch_key}|[f=flv:onfail=ignore]{youtube_url}{youtube_key}"

    # cmd = f"ffmpeg -re -i {source} -f flv {url_primary}/{key} -threads:v 0 -threads:a 0 -filter_threads 2"
    # cmd = "ffmpeg -threads:v 0 -threads:a 0 -filter_threads 2 -thread_queue_size 512 -i %s -f flv %s/%s" % (source, url_primary, key)

    if debug == "true":
        cmd = f"ffmpeg -loglevel debug \
                    -re -i {source} -flags +global_header \
                    -g 50 -c:v libx264 -preset ultrafast -c:a aac -flags +global_header \
                    -f tee -map 0 {streams}"
    else:
        cmd = f"ffmpeg  \
                -re -i {source} -flags +global_header \
                -g 50 -c:v libx264 -preset ultrafast -c:a aac -flags +global_header \
                -f tee -map 0 {streams}"

    result = subprocess.Popen(cmd, shell=True)
    print("\t Streaming finished")
    while result.poll() is None:
        pass
    return True
