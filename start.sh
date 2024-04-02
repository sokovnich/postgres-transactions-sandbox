#!/bin/bash

service ssh start
docker-entrypoint.sh $@
