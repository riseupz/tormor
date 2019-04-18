#!/bin/bash
set -e

echo "Cleaning any existing tormor test database..."
dropdb -h localhost -U postgres tormordb || echo "Tormor database hasn't been created before"
