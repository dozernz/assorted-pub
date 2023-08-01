# Useful Git commands

### List tags and their date:

```
git tag -l --sort=-creatordate --format='%(creatordate:short) %(refname:short)'
```
e.g.

```
2023-07-31 v3.5.12
2023-07-31 v4.0.8
2023-07-31 v4.1.6
2023-07-21 v4.1.5
2023-07-21 v4.0.7
```

### Print git commits at a certain date range:

```
git log --pretty=format:"%H %aI" --after="2018-11-12" --before="2020-12-12"
```

e.g.

```
49eb4d4ddf61e25c5aaab89aa630ddd3c7f3c23d 2020-12-10T06:27:26+01:00
9669167aaeaa834dcc99fa7df961c4f9b8118850 2020-12-09T19:16:30+01:00
127c543a6e59d20de68e6760e952d18ed53578e9 2020-12-08T21:34:17-06:00
f379a52d745dbd765b4ba1fb3133ed6fad3e7c1b 2020-12-09T12:33:33+09:00
```

### Reset all tracked files to their current commited state, and delete everything else:

```
git reset --hard HEAD
git clean -fdx
```
