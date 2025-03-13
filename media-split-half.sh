#!/bin/bash

HALF="323"

for f in *.mkv; do
  new1=$(echo "$f" | sed -r 's/^(.*S[0-9]{2}E)([0-9]{2})E[0-9]{2}.*(\.mkv)$/\1\2.AAAAAAAAAA\3/')
  new2=$(echo "$f" | sed -r 's/^(.*S[0-9]{2})E[0-9]{2}E([0-9]{2}).*(\.mkv)$/\1E\2.AAAAAAAAAA\3/')
  ffmpeg -i "$f" -t "$HALF" -c copy "$new1"
  ffmpeg -ss "$HALF" -i "$f" -c copy "$new2"
  rm -v $f
done
