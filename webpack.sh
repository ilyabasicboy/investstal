#!/bin/bash

PORT=8000

if [ "$1" == "start" ] && [[ $2 == +([0-9]) ]]; then
   PORT=$2
   OPTS=$3
else
   OPTS=$2
fi

docker run --rm --init --interactive --tty \
   -e IS_DOCKER="1" -p $PORT:8000 \
   --add-host=host.docker.internal:host-gateway \
   --volume /workdir/node_modules --volume $(pwd):/workdir \
   redsolution/webpack:default $1 $OPTS