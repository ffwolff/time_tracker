# TimeTracker - Aplicativo de Produtividade com Pomodoro

O **TimeTracker** é um aplicativo web desenvolvido em **Python + Flask** com um frontend reativo utilizando **HTMX**. Seu objetivo é ajudar usuários a gerenciar tarefas e melhorar sua produtividade com o método **Pomodoro**.

Este projeto foi pensado para rodar em ambientes com **restrições de instalação** (sem privilégios de administrador) e utiliza ferramentas leves e de fácil implantação.

---

## Escopo do Projeto

- Cadastro e listagem de tarefas
- Início e controle de sessões Pomodoro (25/5)
- Histórico de sessões com data e duração
- Visualização de produtividade com gráfico
- Backend em Flask com SQLite
- Frontend responsivo com HTML, CSS e HTMX (sem frameworks pesados)
- Totalmente funcional localmente

---

## Tecnologias Utilizadas

### Backend
- **Python 3.x**
- **Flask**
- **SQLite3** (banco embutido no Python)

### Frontend
- **HTMX** – HTML dinâmico com requisições AJAX sem JS complexo
- **HTML5 + CSS3**
- **Chart.js** (para visualização de produtividade)

### Extras
- **Jinja2** (templates do Flask)
- **VS Code** como editor principal
- **Git/GitHub** para versionamento

---

## Estrutura de Pastas

```
time_tracker/
├── app.py # Backend principal com Flask
├── templates/ # HTMLs com Jinja2 + HTMX
│ ├── layout.html
│ ├── index.html
│ └── history.html
├── static/
│ ├── style.css
│ └── script.js
├── database.db # Banco de dados SQLite local
├── requirements.txt # Dependências do projeto
└── README.md # Este documento
```


---

## Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/time_tracker.git
cd time_tracker
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
.\venv\Scripts\activate  # No Windows
```

### 3. Instale as dependências

```bash
pip install --user -r requirements.txt

```

## Como Executar o Projeto

## 1. Execute o servidor Flask

```bash
python app.py
```

## 2. Acesse o navegador

```cpp
http://127.0.0.1:5000
```

Você verá a interface web do TimeTracker rodando localmente.

## Explicação Técnica

`app.py`
- Define as rotas principais (/, /add, /start, /history)
- Manipula o banco de dados SQLite (database.db)
- Usa Flask + renderização com Jinja2

`templates/`
- HTMLs responsivos com inclusão de layout.html
- HTMX permite chamadas assíncronas (ex: iniciar Pomodoro sem recarregar a página)

`static/`
- Estilo do site (style.css)
- Scripts JS opcionais (como timer ou gráficos com Chart.js)

`requirements.txt`
```txt
flask
```

## Funcionalidades

- Sem necessidade de login, mas pode ser estendido
- Pode exportar o histórico como CSV
- Fácil deploy no Render.com (backend) e GitHub Pages (frontend)

## Licença

Este projeto está licenciado sob a **MIT License** – consulte o arquivo `LICENSE` para detalhes.