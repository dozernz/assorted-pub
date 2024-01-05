#!/bin/bash
#set -x

AUTH="$1"

HOST="https://quay.io"
U="v2/_catalog"
for i in {1..100}; do
#echo $U
curl  -D htmp -s -H $'User-Agent: docker/17.09.0-ce go/go1.8.4 git-commit/afdb6d4 kernel/4.14.11-coreos os/linux arch/amd64 UpstreamClient(Docker-Client/17.09.0-ce \\(linux\\))' -H $'Accept: application/vnd.docker.distribution.manifest.v1+prettyjws' -H $'Accept: application/json' -H $'Accept: application/vnd.docker.distribution.manifest.v2+json' -H $'Accept: application/vnd.docker.distribution.manifest.list.v2+json' -H "Authorization: Bearer $AUTH" "$HOST/$U"
URL=$(cat htmp | sed -n -E 's/link:.*<(.*?)>; rel="next".*/\1/p')
#echo $URL
U=$URL
#L=`echo $RES | grep link`
#echo $L
echo $RES
done | jq -r '.repositories[]'
