#!/bin/sh
#
# Run all tests
#

MODULES="camera.py controls.py core.py data.py graphics.py player.py script.py shaders.py"
CHECKER="nosetests"
COVERAGE="python-coverage"
PARAMS="--with-coverage"

if ! hash ${CHECKER} 2>/dev/null
then
    echo "You need to install ${CHECKER} program."
    exit 1
fi

if ! hash ${COVERAGE} 2>/dev/null
then
    echo "You need to install ${COVERAGE} program."
    exit 1
fi

${CHECKER} ${PARAMS}

exit $?
