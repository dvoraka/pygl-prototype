#!/bin/sh
#
# Code layout checker
#

MODULES="camera.py controls.py core.py data.py graphics.py player.py script.py shaders.py"
CHECKER="flake8"
PARAMS="--max-complexity 12"

if ! hash ${CHECKER} 2>/dev/null
then
    echo "You need to install ${CHECKER} program."
    echo "For example:"
    echo "\t\$ pip install ${CHECKER}"
    exit 1
fi

${CHECKER} ${PARAMS} ${MODULES}

exit $?
