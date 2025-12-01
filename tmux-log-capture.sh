#!/bin/bash
#captures all the scrollback from every open tmux session/window/pane to files on disk
#can capture ANSI color etc by adding the -e flag to tmux capture-pane. Can get raw bytes without line reflow by dropping the -J flag.

dir="$HOME/tmuxlogs"; mkdir -p "$dir"
tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}' |
while read -r pane; do
  f="$dir/${pane//[:.]/_}.log"
  tmux capture-pane -J -S - -E - -p -t "$pane" > "$f"
done
