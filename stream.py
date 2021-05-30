import subprocess


def streaming(key, url_primary, source, url_backup=None):
    VBR = 2500
    FPS = 30
    QUAL = "medium"

    cmd = "ffmpeg -loglevel debug -threads:v 2 -threads:a 8 -filter_threads 2 -thread_queue_size 512 -i %s -f flv %s/%s" % (
              source, url_primary, key)
    print(cmd)
    result = subprocess.Popen(cmd, shell=True)
    while result.poll() is None:
        ...
    return


if __name__ == "__main__":
    streaming("7032-mamx-jrgp-e9eh-303k",
              "rtmp://a.rtmp.youtube.com/live2",
              source='"03-11-2020 Statistica.m4v"')
