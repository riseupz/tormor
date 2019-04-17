#!/bin/bash
set -e

dropdb -h localhost -U postgres tormordb || echo "Tormor database hasn't been created before"
createdb -h localhost -U postgres -O postgres tormordb