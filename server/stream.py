import os
import subprocess
import time
import server_cfg

########################## STATIC INT #############################
HOME = "/home/ubuntu/RC/"
SEP = "<SEPARATOR>"
encoding = 'utf-8'


###################################################################

def streaming(user, filename):
    print("\t Streaming started")
    cfg = server_cfg.read_cfg(user)
    preset = cfg["DEFAULT"]["current_preset"].strip()

    source = (f"{HOME}encoded{os.sep}{user}{os.sep}{filename}")
    """n_default = len(cfg["DEFAULT"].keys())
    streams = '"'
    for i in range(len(cfg["stream"].keys())):
        key = list(cfg["stream"].keys())
        key = key[i]
        value = cfg["stream"][key]
        if key not in list(cfg["DEFAULT"].keys()):
            if i%2==0:
                streams += f"[f=flv:onfail=ignore]{value}"
            elif i < len(cfg["stream"].keys())-n_default:
                if i == len(cfg["stream"].keys())-n_default-1:
                    streams += f"{value}\""
                else:
                    streams += f"{value}|"
            if i == len(cfg["stream"].keys())-n_default:
                streams += '"'
    #streams = f'"{streams}"'
    print(f"\n\n\t{streams}\n\n")"""

    youtube_url = cfg[preset]["youtube_url"]
    youtube_key = cfg[preset]["youtube_key"]
    twitch_url = cfg[preset]["twitch_url"]
    twitch_key = cfg[preset]["twitch_key"]
    debug = cfg.getboolean(preset, 'debug')

    streams = f"\"[f=flv:onfail=ignore]{youtube_url}{youtube_key}|[f=flv:onfail=ignore]{twitch_url}{twitch_key}\""

    # cmd = f"ffmpeg -re -i {source} -f flv {url_primary}/{key} -threads:v 0 -threads:a 0 -filter_threads 2"
    # cmd = "ffmpeg -threads:v 0 -threads:a 0 -filter_threads 2 -thread_queue_size 512 -i %s -f flv %s/%s" % (source, url_primary, key)

    if debug:
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
    return True
