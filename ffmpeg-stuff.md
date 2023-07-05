# FFmpeg useful commands:

Crop part of a video: - filter  with `crop=out_width:out_height:start_x:start_y`

```
ffmpeg -y -i in.mov -filter:v "crop=1280:1440:1280:1440" out.mp4
```

Trim:

ss: starting timestamp (hh:mm:ss.xxx)
t: duration from ss
or to: end timestamp

This has no copy flag so it will re-encode.
```
same:
ffmpeg -y -i in.mov -ss 00:03:40 -t 00:01:00 out.mp4
ffmpeg -y -i in.mov -ss 00:03:40 -to 00:04:40 out.mp4
```

* Copy: `-c:v copy`
* No audio: `-an`

Can lead to choppy video

```
ffmpeg -y -i in.mov -c:v copy -an out.mp4
```
