#!/bin/bash

source docker/common.env

UID=$(id -u)
export UID

set -ex

exec docker compose "$@"
