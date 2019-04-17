#!/bin/bash
set -eux

TEST_DBNAME='tormor'

bash ./tests/bootstrap.sh
#!pytest ./tests
# bash ./tests/cleanup.sh