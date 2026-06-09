Projeto de Engenharia de Dados – Análise de Listings do Reverb

Objetivo

Construir um pipeline de dados para coletar informações de anúncios da plataforma Reverb, armazenar os dados na nuvem e realizar transformações para análise e geração de insights.

Arquitetura

O projeto segue as seguintes etapas:

Extração de dados da API do Reverb.
Armazenamento dos dados brutos na AWS S3.
Integração dos dados armazenados com a plataforma Nekt.
Transformação, tratamento e enriquecimento dos dados.
Criação de tabelas analíticas e novas features para consumo analítico.
Fluxo de Dados

API Reverb → Python (Extração) → AWS S3 (Raw Layer) → Nekt (Camadas Bronze, Silver e Gold) → Análise

Tecnologias Utilizadas
Python
Pandas
Requests
ArgParse
SQL
AWS S3
Nekt
Git
GitHub
Conda
Fonte de Dados

API oficial do Reverb:

https://api.reverb.com/api/listings

Estrutura do Projeto
reverb/
├── collect.py
├── sender.py
├── transform.py
├── main.py
├── .gitignore
└── README.md

Funcionalidades
Coleta de dados via API REST.
Armazenamento dos dados brutos em AWS S3.
Organização dos dados em arquitetura de camadas (Bronze, Silver e Gold).
Transformações SQL na Nekt.
Criação de tabelas analíticas para exploração e análise de dados.

