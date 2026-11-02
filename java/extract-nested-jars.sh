#!/usr/bin/env bash
set -euo pipefail

ROOT=$(realpath "${1:-.}")
N="${2:-4}"
CFR="$HOME/tools/cfr-0.153-SNAPSHOT.jar"
OUT="$(pwd)/decompiled"

mkdir -p "$OUT"
export CFR OUT

find "$ROOT" -path "$OUT" -prune -o -type f -iname '*.jar' -print0 |
    xargs -0 -r -P "$N" -n 1 bash -c '
        jar="$1"
        name=$(basename "${jar%.[jJ][aA][rR]}")
        dest="$OUT/$name"

        echo "Decompiling: $jar"

        java -jar "$CFR" --outputdir "$dest" "$jar" 2>&1 |  grep --line-buffered -Fv "Processing " || true
    ' _
