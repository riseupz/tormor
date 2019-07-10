#!/bin/bash
set -e

echo "Creating database for testing..."
createdb -h localhost -U postgres -O postgres tormordb