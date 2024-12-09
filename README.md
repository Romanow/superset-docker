# Apache Superset docker image

[![Build project](https://github.com/Romanow/superset-docker/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/Romanow/superset-docker/actions/workflows/build.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Запуск

Запустить Apache Superset: `dcoker compose up -d --wait`.

Открыть [localhost:8088](http://localhost:8088), логин `program`, пароль `test`.

Открыть любой dashboard, нажать `...` -> `Embed dashboard` -> `Enable Embededing`, скопировать ID
в [superset-embedded](superset-embedded/src/App.tsx).

Запустить superset-embedded: `npm start`, открыть [localhost:3000](http://localhost:3000), должен появиться dashboard.

![Apache Superset Embedded Dashboard](images/Apache%20Superset%20Embedded%20Dashboard.png)
