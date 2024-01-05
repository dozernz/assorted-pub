#!/bin/bash
#set -x

echoerr() { printf "%s\n" "$*" >&2; }

IMG=$1

TAGS=`skopeo list-tags docker://$IMG | jq '.Tags[]' -r | tail -n 20`
TC=`echo "$TAGS" | wc -l`
echoerr "Got $TC tags, pulling dates"
for t in $TAGS
do 
    JJ=".Created, \" $t\n\""
    echo "skopeo inspect -n docker://$IMG:$t | jq -j '$JJ'"
done | parallel -j10 | sort -n | tail -n 1

#| sort -n
