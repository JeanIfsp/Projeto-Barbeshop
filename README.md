# Projeto Barbershop

Este projeto suporta a versão do python especificamente a versão 3.10

## Estrutura do Projeto

```
├── Dockerfile
├── README.md
├── docker-compose.yml
├── env-sample
└── src
    ├── accounts
    ├── barbershop
    ├── chatbot
    ├── core
    ├── manage.py
    ├── requeriments.txt
    ├── static
    ├── templates
    └── venv
```  
## Tecnologias

* Django: Framework de backend para desenvolvimento da aplicação.
* MySQL: Banco de dados relacional.
* Redis: Cache e suporte para sessões em tempo real.

sudo docker run -it -p 8000:8000 -v "$PWD"/src:/app  teste python3 manage.py runserver 0:8000