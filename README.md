<img src="https://raw.githubusercontent.com/BennerLukas/biblio/main/doc/Design/svg/Logo.svg" alt="Logo" width="200"/>

[![GitHub issues](https://img.shields.io/github/issues/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/issues)
[![GitHub forks](https://img.shields.io/github/forks/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/network)
[![GitHub stars](https://img.shields.io/github/stars/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/stargazers)
[![GitHub license](https://img.shields.io/github/license/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/blob/main/LICENSE)

# Biblio

![Python](https://img.shields.io/badge/Language-Python-green?style=flat&logo=python)
![Postgres](https://img.shields.io/badge/DB-Postgres-green?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Container-Docker-green?style=flat&logo=docker)
![Flask](https://img.shields.io/badge/WebFramework-Flask-green?style=flat&logo=flask)

Biblio is a tool for your private library. It manages your books and magazines.


## Using

```bash
docker container run -p 5433:5432 --network dock-net --name biblio -e POSTGRES_PASSWORD=1234 postgres:12.2 
````
