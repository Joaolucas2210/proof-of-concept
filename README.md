# Python PoC: Processamento de Dados XLSX e Integração com PostgreSQL

## Índice

1. [Visão Geral](#visão-geral)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Configuração do Ambiente](#configuração-do-ambiente)
    - [3.1. Ambiente Virtual (Local)](#31-ambiente-virtual-local)
    - [3.2. Docker](#32-docker)
        - [3.2.1. Dockerfile](#321-dockerfile)
        - [3.2.2. docker-compose.yml](#322-docker-composeyml)
4. [Execução da Aplicação](#execução-da-aplicação)
    - [4.1. Executando Localmente](#41-executando-localmente)
    - [4.2. Executando com Docker](#42-executando-com-docker)
5. [Rodando os Testes](#rodando-os-testes)
    - [5.1. Executando Localmente](#51-executando-localmente)
    - [5.2. Executando com Docker](#52-executando-com-docker)
6. [Perguntas e Respostas](#perguntas-e-respostas)
    - [1. Padrões de Projeto Utilizados](#1-padrões-de-projeto-utilizados)
    - [2. Princípios SOLID Aplicados](#2-princípios-solid-aplicados)
    - [3. Ponto Mais Desafiador no Desenvolvimento](#3-ponto-mais-desafiador-no-desenvolvimento)
7. [Considerações Finais](#considerações-finais)
8. [Recursos](#recursos)
9. [Contato](#contato)

---

## Visão Geral

Este projeto é uma **Proof of Concept (PoC)** desenvolvida em Python que demonstra a leitura de arquivos XLSX, processamento e agregação de dados utilizando `pandas`, e persistência dos resultados em um banco de dados PostgreSQL. A aplicação segue boas práticas de desenvolvimento, empregando Programação Orientada a Objetos (OOP) e princípios SOLID para garantir um código claro, bem estruturado e de fácil manutenção. Além disso, todo o ambiente é containerizado utilizando Docker para garantir portabilidade e consistência entre diferentes ambientes de desenvolvimento.

### Funcionalidades

1. **Leitura de Arquivo XLSX**: Utiliza `pandas` para ler dados estruturados de uma planilha Excel.
2. **Processamento e Agregação de Dados**:
    - Cruzamento de dados somando todos os anos disponíveis.
    - Tabelas cruzadas:
        - Sexo x Local
        - Local x Idade
        - Sexo x Idade
3. **Persistência de Dados**: Insere os resultados das tabelas cruzadas em um banco de dados PostgreSQL.
4. **Testes Automatizados**: Implementação de testes unitários utilizando `pytest` e mocks para garantir a qualidade e funcionalidade do código.
5. **Containerização com Docker**: Facilita a execução da aplicação e dos testes em ambientes isolados e consistentes.

---

## Estrutura do Projeto

```bash
meu_projeto/
├── Dockerfile
├── docker-compose.yml
├── docker-compose.test.yml
├── requirements.txt
├── src/
│   ├── main.py
│   ├── config.py
│   ├── services/
│   │   └── data_service.py
│   ├── repository/
│   │   ├── base_repository.py
│   │   └── result_repository.py
│   ├── models/
│   │   └── result_model.py
│   └── utils/
│       └── xlsx_reader.py
└── tests/
    ├── test_data_service.py
    └── test_xlsx_reader.py

