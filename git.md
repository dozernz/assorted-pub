# Useful Git commands

### Search all git file history for a string

```
git --no-pager grep -i "stringtofind" $(git rev-list --all)
```

This also supports the "-C <N>" context flag to print the <N> surrounding lines

Unique matches only:

```
git --no-pager grep -i -h "stringtofind" $(git rev-list --all) | sort -u
```

### Commits newer than a certain date range

One year ago:

```
git rev-list --since="1 year ago" --all
```

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

### Search the entire code history for the first instance of a string:

```
git --no-pager log -S'stringtofind' --source --all --pretty=tformat:"%H %aI"
```

e.g.

```
$ git --no-pager log -S'stringtofind' --source --all --pretty=tformat:"%H %aI" 
12a6cf569e042c0d6420be3778d7a793460693c4 2023-07-27T07:13:45-07:00
```
