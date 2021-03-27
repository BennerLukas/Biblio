<img src="https://raw.githubusercontent.com/BennerLukas/biblio/main/doc/Design/svg/Logo.svg" alt="Logo" width="200"/>

[![GitHub issues](https://img.shields.io/github/issues/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/issues)
[![GitHub forks](https://img.shields.io/github/forks/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/network)
[![GitHub stars](https://img.shields.io/github/stars/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/stargazers)
[![GitHub license](https://img.shields.io/github/license/BennerLukas/biblio)](https://github.com/BennerLukas/biblio/blob/main/LICENSE)

# Biblio

<div>
<img src="/doc/Design/svg/Logo.svg" alt="Logo" width="400" align="center"/>
</div>

![Postgres](https://img.shields.io/badge/DB-Postgres-lightgrey?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Container-Docker-lightgrey?style=flat&logo=docker)

![Flask](https://img.shields.io/badge/WebFramework-Flask-lightgrey?style=flat&logo=flask)
![Flask](https://img.shields.io/badge/Framework-Bootstrap-lightgrey?style=flat&logo=bootstrap)

![Python](https://img.shields.io/badge/Language-Python-lightgrey?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Language-HTML-lightgrey?style=flat&logo=html5)
![Flask](https://img.shields.io/badge/Language-CSS-lightgrey?style=flat&logo=css3)

Biblio is a tool for your private library. It manages your books and magazines.


## Using
First create a database container:
```bash
docker container run -p 5433:5432 --name biblio -e POSTGRES_PASSWORD=1234 postgres:12.2 
````

Then init the biblio databse by running :
```bash
cd src/api
python biblio.py
```

After that start the flask server by:
```bash
cd src/
python run.py
```

## Docker Container

Otherwise you can use the docker-image provided in the repository.


## About the project

### Team
- [Lukas Benner](https://github.com/BennerLukas)
- [Phillip Lange](https://github.com/Sabokou)
- [Alina Buss](https://github.com/Alinabuss)

### Target
With Biblio we want to build a system to keep track of your private book collection like its a real library.

Biblio is your tool to manage your own private book collection. Whether you want to keep track of all your books. Find gems you forgot about or keep track of your reading list. With Biblio you can also invite friends and family to your private library. It allows you to share and borrow books between each other.

We think its important to know your possessions and keep it managed. We can help you to focus on reading rather than searching. On the other hand its very important to share, so everybody can enjoy reading and learning new stuff. Biblio helps you to organize this process easily.


### Tools
For developing Biblio we used Python, Flask, Postgres and a little bit of bootstrap for easier styling.
 
## Presentation
<div>
<img src="/doc/Design/screenshots/Screenshot%202021-03-27%20203035.png" alt="Screenshot" width="800"/>
<br>
<img src="/doc/Design/screenshots/Screenshot%202021-03-27%20203102.png" alt="Screenshot" width="800"/>
<br>
<img src="/doc/Design/screenshots/Screenshot%202021-03-27%20203118.png" alt="Screenshot" width="600"/>
<br>
</div>