#!/bin/bash
set -x
IMG=$1

skopeo list-tags docker://$IMG | jq '.Tags[]' -r
