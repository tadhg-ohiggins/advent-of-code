#!/bin/zsh

if [[ $# -eq 0 ]] then
    echo "No answer!"
    exit 1
fi

python ../../resources/python/submit.py ${@} --part 1
python ../../resources/python/fetch.py;
