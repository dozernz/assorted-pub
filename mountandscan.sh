#!/bin/bash

for i in `ls ../img/`
do
echo $i
dwarfs -o workers=8,readonly ../img/$i tmp/
~/Desktop/trufflehog  --no-update --no-verification --concurrency=25  --exclude-detectors=`cat ~/Desktop/EXCLUDESNP` filesystem -x ~/Desktop/excludeddirs tmp 2>/dev/null
umount tmp
done
