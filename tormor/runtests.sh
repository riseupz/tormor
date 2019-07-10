#!/bin/bash
set -eux

bash ./tests/cleanup.sh
bash ./tests/bootstrap.sh
pytest -v
