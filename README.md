# Projeto Integrado Multidisciplinar (PIM)

# 🎓 Entre Conexões

Uma plataforma educacional digital e modular que integra alunos e professores em um ambiente funcional, promovendo uma experiência de aprendizagem eficiente, moderna e organizada.

---

## 📌 Objetivo

O principal objetivo do projeto é oferecer uma estrutura escalável, de fácil manutenção, que organiza e distribui conteúdos didáticos de maneira lógica e acessível.

---

## ⚙️ Tecnologias Utilizadas

- **Python** – Lógica principal e funções da plataforma
- **JSON** – Armazenamento e estruturação de dados
- **PDF (via Python)** – Geração de relatórios e materiais didáticos
- **Canva** – Criação de materiais visuais (PDFs)

---

## 📂 Estrutura do Projeto

```
entre-conexoes/
│
├── assets/         # Imagens e arquivos visuais (ex: PDFs educativos)
├── data/           # Arquivos JSON (usuários, trilhas, módulos, conteúdos, quizzes)
├── modules/        # Funções reutilizáveis em Python
├── pdf/            # Geração e armazenamento de relatórios PDF
└── src/            # Código principal e lógica do sistema (menus, navegação)
```

---

## 🧭 Funcionalidades Principais

### 👤 Cadastro e Login

- Registro de novos usuários com criptografia de senha (SHA-256)
- Login seguro com verificação de dados

### 🧠 Trilhas e Módulos Educacionais

- Sistema de trilhas de conhecimento com progresso por módulos
- Restrições de acesso baseado na ordem de conclusão
- Realização de quizzes com verificação automática de acertos

### 📊 Estatísticas Educacionais

- Análise de desempenho dos alunos por trilha
- Cálculo de média, moda e mediana dos módulos concluídos
- Relatórios no terminal para feedback pedagógico

---

## 🖥️ Execução

1. Clone o repositório:

git clone https://github.com/vinicimxt/PIM.git

2. Execute o arquivo principal dentro da pasta `src`.

---

"Realiza o registro de novos usuários, salvando os dados em JSON com senha criptografada."""


---

## 🧩 Contribuindo

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto
2. Crie uma nova branch: `git checkout -b feature/nova-feature`
3. Faça commit das suas alterações: `git commit -m 'Adiciona nova feature'`
4. Push para o fork: `git push origin feature/nova-feature`
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

---

## 📎 Materiais Complementares

Os materiais visuais em PDF foram elaborados com o Canva, alinhados à identidade visual da plataforma.

---

## ✅ Considerações Finais

O projeto **Entre Conexões** foi estruturado com foco em modularidade, boas práticas de programação e organização de conteúdo. Ele pode ser facilmente expandido e utilizado em diferentes contextos educacionais.
