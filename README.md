
# 🚀 API de Rede Social

Uma API RESTful robusta e completa para uma rede social, desenvolvida utilizando **FastAPI** e **SQLAlchemy**. O projeto foi construído seguindo as melhores práticas de mercado, utilizando uma arquitetura em camadas (Routers, Services, Models e Schemas) para garantir manutenibilidade, segurança e escalabilidade.

---

## 🛠️ Tecnologias Utilizadas

* **[FastAPI](https://fastapi.tiangolo.com/):** Framework web moderno, rápido (alta performance) e de fácil codificação baseado em Python.
* **[SQLAlchemy](https://www.sqlalchemy.org/):** O ORM Python mais utilizado para mapeamento das tabelas do banco de dados.
* **[Pydantic](https://docs.pydantic.dev/):** Validação de dados e gerenciamento de configurações através de Schemas estruturados.
* **[Alembic](https://alembic.sqlalchemy.org/):** Ferramenta de migração de banco de dados leve para uso com o SQLAlchemy.
* **[Uvicorn](https://www.uvicorn.org/):** Servidor ASGI de alta performance para rodar a aplicação.

---

## Arquitetura do Projeto

A estrutura de pastas foi dividida seguindo o padrão de separação de conceitos:

```text
api-rede-social/
├── app/
│   ├── core/          # Configurações globais e segurança (JWT, hash de senhas)
│   ├── models/        # Modelos do banco de dados (SQLAlchemy)
│   ├── routers/       # Endpoints da API divididos por recursos (FastAPI Routers)
│   ├── schemas/       # Validação de dados de entrada/saída (Pydantic Models)
│   ├── services/      # Camada com as regras de negócio e persistência no banco
│   ├── database.py    # Configuração e sessão do banco de dados
│   └── main.py        # Ponto de entrada da aplicação
├── alembic/           # Arquivos de migração histórica do banco de dados
├── uploads/           # Armazenamento de arquivos locais (Avatares, mídias)
└── requirements.txt   # Lista de dependências do projeto

## Como Rodar o Projeto Localmente

git clone [https://github.com/moisesvinicius0101/api-rede-social.git](https://github.com/moisesvinicius0101/api-rede-social.git)
cd api-rede-social

## Configurar o Ambiente Virtual (venv)

# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente (Windows)
.\venv\Scripts\activate

# Ativar o ambiente (Linux/MacOS)
source venv/bin/activate

## Instalar as Dependências

pip install -r requirements.txt

## Rodar as Migrations (Criar as Tabelas)

alembic upgrade head

## Iniciar Servidor
uvicorn app.main:app --reload

Autor: Moises Vinicius💻