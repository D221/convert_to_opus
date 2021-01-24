#!bin/bash
trap "exit" INT # allows to terminate anytime
set -e # quits on error
echo "Type in the directory to convert"
read -r dir
cd "$dir"
echo "Type in original file type"
read ext
echo "Prefered bitrate (in kbps)"
read rate
mkdir original
for i in *.$ext; do
  echo "Converting "$i
  ffmpeg -loglevel panic -i "$i" -c:a libopus -b:a "$rate"k -vbr on "${i%.*}.opus"
  mv "$i" original
done
