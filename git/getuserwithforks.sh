#!/bin/bash

UACC=$1

function echoerr() { echo "$@" 1>&2; }

threshold=250


rl_rem=`gh api rate_limit | jq '.rate.remaining'`
if [ "$rl_rem" -lt "$threshold" ]; then
    current_time=$(date +%s)
    epoch_time=`gh api rate_limit | jq '.rate.reset'`
    sleep_duration=$((epoch_time - current_time + 25))
    echoerr "sleeping for $sleep_duration"
    sleep $sleep_duration
fi

gh api --paginate -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "/users/$UACC/repos?per_page=100" | jq '.[] | .clone_url' -r
