#!/bin/bash

url="$1"

while [ -n "$url" ]; do
    response=$(curl -s -D - "$url")

    # print response body
    echo "$response" | sed '1,/^\r$/d'

    # extract Link header and parse out the next URL
    url=$(echo "$response" | grep -i '^Link:' | sed -n 's/.*<\([^>]*\)>.*/\1/p' | head -n 1)

    # if no more Link header, exit loop
    [ -z "$url" ] && break

    echo "Following: $url"
done
