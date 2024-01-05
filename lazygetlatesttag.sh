#!/bin/bash
#set -x
IMG=$1

TAG=`skopeo list-tags docker://$IMG | jq '.Tags[]' -r | tail -n1`
echo $IMG:$TAG
