# 🧬 Trix

> **Sistema web voltado para a triagem clínica e conscientização sobre a Síndrome do X Frágil.**

---

## 🎯 Sobre o Projeto

O **Trix** (abreviação para *Triagem X*) tem como objetivo principal oferecer assistência técnica computacional e promover a conscientização sobre a **Síndrome do X Frágil (SXF)**, uma condição genética hereditária que afeta milhares de brasileiros.

Através deste sistema web, buscamos otimizar e padronizar o processo de triagem clínica, auxiliando profissionais da saúde na identificação rápida de pacientes com potencial risco para a síndrome e no direcionamento adequado para testes genéticos.

---

## 🎓 Contexto Acadêmico

Este projeto foi idealizado e desenvolvido como parte integrante da disciplina de **Experiência Criativa: Criando Soluções Computacionais**, do curso de **Ciência da Computação** da **Pontifícia Universidade Católica do Paraná (PUCPR)**.

---

## 🎬 Vídeos

| | Link |
|---|---|
| Tutorial da plataforma | [assistir no YouTube](https://www.youtube.com/watch?v=LINK_TUTORIAL) |
| Implantação do sistema | [assistir no YouTube](https://www.youtube.com/watch?v=LINK_IMPLANTACAO) |

---

## 🛠️ Tecnologias Utilizadas

### 🎨 Front-end e UI Design
* **HTML5:** Estruturação semântica e acessível das páginas web.
* **Pico CSS (v2.1.1):** Framework CSS minimalista, utilizado como biblioteca base e importado via tag `<link>` em cada página.
* **CSS Customizado (`style.css`):** Construído sobre o Pico CSS para implementar personalizações visuais exclusivas — paleta de cores, logo, navbar e botões.
* **JavaScript:** Utilizado para máscaras de input e exibição de erros de validação na interface.

### ⚙️ Back-end e Banco de Dados
* **Python 3.10+:** Linguagem principal para a lógica de negócio e estruturação do back-end.
* **FastAPI:** Framework web para construção das rotas e APIs.
* **SQLAlchemy:** ORM utilizado como mapeador das tabelas do banco.
* **Pydantic:** Validação de dados no back-end.
* **MySQL 8.0+:** Banco de dados relacional para armazenar usuários, pacientes e históricos de avaliações.

### 💻 Ferramentas de Desenvolvimento
* **Visual Studio Code (VS Code):** Editor de código-fonte principal utilizado pela equipe.
* **MySQL Workbench:** Gerenciador visual para modelar, administrar e consultar o banco de dados.
* **Google Chrome:** Navegador utilizado para testar e validar o sistema (versão mais recente compatível).

---

## 📋 Requisitos do Sistema

| Componente | Versão | Observação |
|---|---|---|
| Sistema Operacional | Windows 11 Pro 24H2 | Testado nesta versão |
| Python | 3.10 ou superior | Testado com 3.14.3 |
| MySQL | 8.0 ou superior | Deve estar rodando antes de iniciar |
| Google Chrome | 149.0.7827.55 | Testado nesta versão |

### Dependências Python

Instaladas automaticamente via `pip install -r requirements.txt`.

| Pacote | Versão |
|---|---|
| fastapi | >=0.111, <1.0 |
| uvicorn | >=0.30, <1.0 |
| sqlalchemy | >=2.0, <3.0 |
| pydantic | >=2.7, <3.0 |
| pymysql | >=1.1, <2.0 |
| python-multipart | >=0.0.9, <1.0 |
| python-dotenv | >=1.0, <2.0 |
| jinja2 | >=3.1, <4.0 |
| itsdangerous | >=2.1, <3.0 |

---

## 🚀 Instalação e Execução Local

### Pré-requisitos

- Python 3.10 ou superior instalado e no PATH
- MySQL 8.0 ou superior **rodando** na máquina
- Um usuário MySQL com permissão para criar databases (ex.: `root`)

### Passo 1 — Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
DATABASE_URL=mysql+pymysql://USUARIO:SENHA@localhost:3306/trix
SECRET_KEY=escolha-uma-chave-secreta-longa
```

> Se a senha tiver caracteres especiais, codifique-os na URL.
> Exemplo: `exemplo@1234` → `exemplo%401234`

### Passo 2 — Criar e ativar ambiente virtual

```bash
python -m venv .venv
```

```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### Passo 3 — Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 4 — Criar e popular o banco de dados

Abra o **MySQL Workbench** (ou outro cliente MySQL) e execute os scripts da pasta `database/` **nesta ordem**:

1. `setup_banco.sql`: cria o banco `trix` do zero.
2. `schemas.sql`: cria todas as tabelas.
3. `inserts.sql`: insere os dados de demonstração.

Ao final, o banco `trix` estará criado, com as tabelas e os dados iniciais prontos para uso.

### Passo 5 — Iniciar o servidor

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8080
```

Acesse no navegador: **http://127.0.0.1:8080**

---

## 🔑 Credenciais Iniciais

| Login | Senha | Perfil |
|---|---|---|
| `admin` | `admin123` | Administrador |
| `dra.ana` | `ana123` | Médico |

---

## 📚 Documentação

A modelagem do banco de dados, com os modelos conceitual, lógico e físico, está descrita em [documentacao.md](documentacao.md).

---

## 📁 Estrutura do Projeto

```
/
├── database/
│   ├── setup_banco.sql   ← cria o banco trix (DROP/CREATE)
│   ├── schemas.sql       ← estrutura das tabelas (modelo físico)
│   └── inserts.sql       ← dados iniciais de demonstração
├── docs/                 ← diagramas do banco (conceitual e lógico)
├── static/               ← CSS, JS, imagens
├── templates/            ← páginas HTML (Jinja2)
├── .gitignore
├── crud.py               ← operações de banco
├── db.py                 ← conexão (engine/session)
├── documentacao.md       ← modelagem do banco (conceitual, lógico, físico)
├── main.py               ← rotas do FastAPI
├── models.py             ← mapeamento das tabelas (SQLAlchemy Mapper)
├── paginas_html.py       ← renderizador Jinja2
├── README.md
├── requirements.txt
└── schemas.py            ← validações (Pydantic)
```

---

## 👥 Equipe Desenvolvedora

O projeto foi construído colaborativamente pelos seguintes estudantes de Ciência da Computação:

* 👨‍💻 **Adrian Arthur**
* 👨‍💻 **Luan Orlovski**
* 👨‍💻 **Lucas Prado**
* 👨‍💻 **Matheus Quadros**
* 👨‍💻 **Vagner Salviano**
* 👨‍💻 **Bruno Albach**

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  <i>Projeto acadêmico - PUCPR | Ciência da Computação</i>
</p>
