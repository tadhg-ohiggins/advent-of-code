#!/bin/zsh

if [[ $# -eq 0 ]] then
    ARGUMENT=$(date -j -v+3H "+%d");
else
    ARGUMENT=${1};
fi

DAYNUM=${(pl:2::0:)ARGUMENT}; # Fun with zsh variable expansion rules.

tmux split-window -h -c "#{pane_current_path}";
tmux select-pane -t .0;
python fetch.py "${DAYNUM}" ${@:2};
tmux send-keys -t .1 "cat data/input-${DAYNUM}.txt";
tmux send-keys -t .1 "python day.py ${DAYNUM}";
nvim -o2 "data/puzzle-${DAYNUM}.md" "days/day-${DAYNUM}.py" "tutil.py"
