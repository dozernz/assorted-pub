# FFmpeg useful commands:

### Add Subtitles

Make a srt file first:
```
1
00:00:00,000 --> 00:00:05,000
Test sub
```
then apply it (requires re-encoding):

```
ffmpeg -y -i in.mp4 -vf subtitles=1.srt out.mp4
```

### Quiet
```
-hide_banner -loglevel error
```

### Crop part of a video: 
filter  with `crop=out_width:out_height:start_x:start_y`

```
ffmpeg -y -i in.mov -filter:v "crop=1280:1440:1280:1440" out.mp4
```

### Trim:

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

Can lead to choppy video?

```
ffmpeg -y -i in.mov -c:v copy -an out.mp4
```

### Concat multiple files without re-encoding

```
ffmpeg -f concat -safe 0 -i <(printf "file '$PWD/%s'\n" ./*.mov) -c copy concat-out.mp4
```

### Resize / scale video
Requires re-encoding

```
ffmpeg -i input.avi -vf scale=1280:720 output.avi
```

Can specify only one dimension to keep aspect ratio:

```
ffmpeg -i input.avi -vf scale=1280:-1 output.avi
```

Some codecs require the size of width and height to be a multiple of n. You can achieve this by setting the width or height to `-n`:
```
ffmpeg -i input.jpg -vf scale=320:-2 output_320.png
```
The output will now be 320×206 pixels.


### Scale with nvidia hwenc:

```
ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i input.mov -vf scale_cuda=1280:720 -c:v h264_nvenc outcuda.mp4
```

### Nvidia HWENC cfr equivalent
Roughly equivalent to crf 23

```
ffmpeg -y -vsync 0 -hwaccel cuda -hwaccel_output_format cuda -i input.mov -vf scale_cuda=1280:720 -profile:v high -c:v h264_nvenc -preset medium -profile:v high -tune hq -level 5.1 -rc vbr -cq 23 outcuda.mp4
```


### Nvidia HWENC presets
Doesn't seem to make much difference on a small video 
Slow: `-preset slow`
video:40686kB
real    0m8.399s

Medium: `-preset medium`
video:41249kB
real    0m6.926s

Fast: `-preset fast`
video:46092kB
real    0m6.885s
