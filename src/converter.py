import os
import shutil
import subprocess


def convert(path, bitrate, original):
    commontypes = ('.flac', '.mp3', '.wav', '.m4a',
                   '.aac', '.webm', '.mp4', '.avi', '.mkv')
    if os.name == 'nt':
        subprocess.CREATE_NO_WINDOW  # no cmd on windows
    if original != 'NONE':
        if not os.path.exists('original'):
            os.makedirs('original')
    for filename in os.listdir(path):
        if (filename.endswith(commontypes)):
            print("Converting "+filename)
            without_ext = os.path.splitext(filename)[0]
            subprocess.call('ffmpeg -i "{0}" -loglevel panic -c:a libopus -b:a {1}k -vbr on "{2}.opus"'.format(
                filename, bitrate, without_ext), shell=True)
            if original == 'NONE':
                os.remove(filename)
            else:
                shutil.move('{0}/{1}'.format(path, filename), original)
        else:
            continue


def convertfile(file, bitrate, original):
    if os.name == 'nt':
        subprocess.CREATE_NO_WINDOW  # no cmd on windows
    print("Converting "+file)
    without_ext = os.path.splitext(file)[0]
    subprocess.call('ffmpeg -i "{0}" -loglevel panic -c:a libopus -b:a {1}k -vbr on "{2}.opus"'.format(
        file, bitrate, without_ext), shell=True)
    if original == 'NONE':
        os.remove(file)
