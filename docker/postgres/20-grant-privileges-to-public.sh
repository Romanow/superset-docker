#!/usr/bin/env bash

set -e

export PGPASSWORD=postgres
psql -U postgres -d superset -c 'GRANT ALL PRIVILEGES ON SCHEMA public TO program;'
psql -U postgres -d examples -c 'GRANT ALL PRIVILEGES ON SCHEMA public TO program;'
