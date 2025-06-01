## 🧾 MEIControle

**MEIControle** é um assistente financeiro com inteligência artificial criado para apoiar **microempreendedores individuais (MEIs)** na gestão simples e intuitiva de seu fluxo de caixa.

Figma: https://www.figma.com/proto/edGhc8O5EB4dJlENEyCLQy/Untitled?node-id=0-1&t=7DTV2mYaGPlxeZiJ-1

O app funciona como um **chat interativo** onde o usuário informa suas movimentações financeiras, como:

```
Gasto de 50 reais em bebidas  
Venda de 123 reais
```

A inteligência artificial interpreta os comandos, classifica como entrada ou saída e armazena as informações. Além disso, o MEIControle pode gerar relatórios financeiros, gráficos e realizar predições de gastos e vendas.

---

## 🚀 Tecnologias Utilizadas

- **Frontend:** Flutter
- **Backend:** FastAPI
- **IA / Processamento de Linguagem Natural:** Python (pspaCy e custom LLM)
- **Banco de Dados:** PostgreSQL
- **Outros:** Pandas, Matplotlib, Scikit-learn (para análise e previsão)

---

## 🧠 Funcionalidades

- Chatbot com IA para registro de entradas/saídas
- Classificação automática dos registros financeiros
- Geração de relatórios com gráficos
- Predição de receitas e despesas futuras
- Exportação de dados em formato CSV
- Interface mobile amigável e prática

---

## 📦 Como Rodar o Projeto

### 🐋 Docker (API)
- Para rodar:
- `docker compose up --watch`
- `docker compose run app /bin/bash`ou `docker compose run app python`
- Para parar o container:
- `docker compose down` ou `docker compose down -v` (remover volumes)


### Flutter (Front-End)
- Para rodar:
- `flutter create .`
- `flutter pub get`
- `flutter run`
---

## 📌 Status do Projeto

> Em desenvolvimento – MVP em construção como parte do projeto integrador **Talento Tech PR 2024**

---

## 👥 Equipe
- Luan Salomão   
[![GitHub followers](https://img.shields.io/github/followers/luanvsalmeida?label=Follow&style=social)](https://github.com/luanvsalmeida)
- Cauã Santos   
[![GitHub followers](https://img.shields.io/github/followers/luanvsalmeida?label=Follow&style=social)](https://github.com/luanvsalmeida)
- Gabriel Carvalho   
[![GitHub followers](https://img.shields.io/github/followers/Gabriel2718?label=Follow&style=social)](https://github.com/Gabriel2718)
- Silvio Henrique   
[![GitHub followers](https://img.shields.io/github/followers/silvioGPS?label=Follow&style=social)](https://github.com/silvioGPS)


---

## 📈 Roadmap

1. **Planejamento e prototipação ✅**
   - Definir funcionalidades MVP
   - Criar protótipo de telas (Figma, etc.)

2. **Criação do chatbot com IA em (SpaCy) 🔍** 
   - Interpretar frases com NLP (entrada/saída + categoria + valor)

3. **Criação da interface Flutter 🛠️**
   - Tela de chat
   - Tela de relatórios (mock inicial)

4. **Integração com backend (Python/FastAPI) 🛠️**
   - API para salvar e recuperar os dados do usuário
   - Autenticação básica

5. **Geração de relatórios ✅**
   - Gráficos com dados financeiros
   - Exportação para PDF/Excel

6. **Predição com ML ✅**
   - Usar dados registrados para prever entradas/saídas futuras

7. **Lembretes de Compromissos ⏳**
   - API lembra o usuário sobre compromissos 

---
