#!/bin/bash

for i in `ls ../img/`
do
echo $i
dwarfs -o workers=8,readonly ../img/$i tmp/
rg -C 3 -i $1 tmp/
umount tmp
done
