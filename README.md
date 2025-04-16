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
- **Backend:** Node.js (opcional, para APIs, autenticação, etc)
- **IA / Processamento de Linguagem Natural:** Python (possivelmente com modelos como spaCy, Transformers ou custom LLM)
- **Banco de Dados:** A definir (sugestões: Firebase, PostgreSQL, MongoDB)
- **Outros:** Pandas, Matplotlib, Scikit-learn (para análise e previsão)

---

## 🧠 Funcionalidades

- Chatbot com IA para registro de entradas/saídas
- Classificação automática dos registros financeiros
- Geração de relatórios com gráficos
- Predição de receitas e despesas futuras
- Exportação de dados em formato PDF/Excel
- Interface mobile amigável e prática

---

## 📦 Como Rodar o Projeto

Em breve.

---

## 📌 Status do Projeto

> Em desenvolvimento – MVP em construção como parte do projeto integrador **Talento Tech PR 2024**

---

## 👥 Equipe

-

---

## 📈 Roadmap (Sugestão de Etapas)

1. **Planejamento e prototipação**
   - Definir funcionalidades MVP
   - Criar protótipo de telas (Figma, etc.)

2. **Criação do chatbot com IA em Python**
   - Interpretar frases com NLP (entrada/saída + categoria + valor)
   - Salvar temporariamente os dados (pode usar SQLite ou JSON)

3. **Criação da interface Flutter**
   - Tela de chat
   - Tela de relatórios (mock inicial)

4. **Integração com backend (Node.js)**
   - API para salvar e recuperar os dados do usuário
   - Autenticação básica

5. **Geração de relatórios**
   - Gráficos com dados financeiros
   - Exportação para PDF/Excel

6. **Predição com ML**
   - Usar dados registrados para prever entradas/saídas futuras

---
