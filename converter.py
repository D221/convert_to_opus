import os
import shutil
import subprocess


def convert(path, bitrate, original):
    commontypes = ('.flac', '.mp3', '.wav', '.m4a', '.aac')
    if os.name == 'nt':
        subprocess.CREATE_NO_WINDOW # no cmd on windows
    for filename in os.listdir(path):
        if (filename.endswith(commontypes)):
            print("Converting "+filename)
            without_ext = os.path.splitext(filename)[0]
            os.system('ffmpeg -i "{0}" -loglevel panic -c:a libopus -b:a {1}k -vbr on "{2}.opus"'.format(
                filename, bitrate, without_ext))
            shutil.move('{0}/{1}'.format(path, filename), original)
        else:
            continue
