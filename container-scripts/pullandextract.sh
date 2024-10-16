#!/bin/bash

IMG=$1
echo "Downloading image $IMG"
#remove registry
REGLESS=`echo $IMG | sed 's/.*\///g'`
echo $REGLESS
TAG=`echo $REGLESS | sed 's/.*://g'`
IM=`echo $REGLESS | sed 's/:.*//g'`
#echo $TAG
#echo $IM

skopeo copy --quiet docker://$IMG oci:/dev/shm/$IM-oci:$TAG
umoci raw unpack --rootless --image /dev/shm/$IM-oci:$TAG /dev/shm/$IM-unpack 2>/dev/null
sudo rm -rf "/dev/shm/$IM-oci"
