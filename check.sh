#!/bin/sh
#
# Code layout checker
#

MODULES="camera.py controls.py core.py data.py graphics.py player.py script.py shaders.py"
CHECKER="flake8"

if ! hash ${CHECKER} 2>/dev/null
then
    echo "You need install ${CHECKER} program."
    exit 1
fi

flake8 ${MODULES}

exit 0
