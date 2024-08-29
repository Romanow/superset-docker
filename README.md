# Apache Superset docker image

[![Build project](https://github.com/Romanow/superset-docker/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/Romanow/superset-docker/actions/workflows/build.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

```shell
$ curl -X POST http://localhost:8088/api/v1/security/login \
    -H 'Content-Type: application/json' \
    -d '{"username": "program","password": "test","provider": "ldap"}'

$ curl -X POST http://localhost:8088/api/v1/security/guest_token/ \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer {{ token }}' \
    -d '{"user": { "username": "guest_user" }, "resources": [{ "type": "dashboard", "id": "{{ embedded_dashboard_id }}" }],"rls":[ ]}'
```