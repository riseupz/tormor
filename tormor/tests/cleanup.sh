#!/bin/bash
set -e

dropdb -h localhost -U postgres tormordb || echo "Tormor database hasn't been created before"
dropuser tormor || echo "No user tormor has been created before"
