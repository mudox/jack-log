#!/usr/bin/env bash
set -euo pipefail

source ~/Git/dot-files/bash/lib/jack

tput civis
trap 'tput cnorm' EXIT

# tty size
set +u
if [[ -n "$TMUX" ]]; then
  tty_width="$(tmux list-clients -t '.' -F '#{client_width}')"
  tty_height="$(tmux list-clients -t '.' -F '#{client_height}')"
else
  tty_width=$(tput lines)
  tty_height=$(tput cols)
fi
set -u

# kill session if exists
session_name='JacLog'
if tmux has-session -t ${session_name} &>/dev/null; then
  jackWarn "session [${session_name}] already exists, kill it!"
  tmux kill-session -t "${session_name}"
fi

#
# window: Edit
#
jackProgress 'Creating window [Edit] ...'

root="${HOME}/Develop/Python/jac-log"
window_name='Edit'
window="${session_name}:${window_name}"
tmux new-session       \
  -s "${session_name}" \
  -n "${window_name}"  \
  -x "${tty_width}"    \
  -y "${tty_height}"   \
  -c "${root}"         \
  -d
sleep 1
tmux send-keys -t "${window}.1" '
v py **/*.py .tmux-session.sh
'

# pane: Edit.2
# at the top right corner
# run testing command
tmux split-window  \
  -t "${window}.1" \
  -h               \
  -c "${root}"

# pane: Edit.3
# at bottom right corner
# `tail -f` testing log out
root="${HOME}/.local/share/test_jaclog/log"
tmux split-window  \
  -t "${window}.2" \
  -v               \
  -c "${root}"
sleep 1
tmux send-keys -t "${window}.3" '
tail -n0 -f test.log
'

tmux select-pane -t "${window}.1"

jackEndProgress
tmux select-window -t "${session_name}:1.1"
echo "[${session_name}]"
tmux list-window -t "${session_name}" -F ' - #W'
