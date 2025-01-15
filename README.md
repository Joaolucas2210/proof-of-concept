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
```

## Configuração do Ambiente
3.1. Ambiente Virtual (Local)
Para rodar a aplicação localmente sem Docker, siga os passos abaixo:

Instale o Python 3.9+:
Certifique-se de que o Python está instalado na sua máquina. Você pode verificar a versão com:
python --version
Crie um Ambiente Virtual:

```python -m venv venv```

Ative o Ambiente Virtual:
Linux/macOS:

```source venv/bin/activate```

Windows:

```.\venv\Scripts\activate```

Instale as Dependências:

```pip install -r requirements.txt```

As dependências estão listadas no requirements.txt e incluem:

```
numpy==1.23.5
pandas==1.5.3
openpyxl==3.1.2
psycopg2==2.9.6
unidecode==1.3.6
pytest
pytest-cov
mock
patch
```
Assim, suas dependências ficam isoladas no ambiente virtual.

# 3.2. Docker
Utilize Docker para garantir que a aplicação e o banco de dados PostgreSQL rodem em ambientes consistentes.

3.2.1. Dockerfile
Define a imagem Docker para a aplicação.

```
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY . /app

# Define o ponto de entrada da aplicação
CMD ["python", "src/main.py"]
````

Base: Utiliza a imagem oficial do Python 3.9 slim.
Dependências: Instala as dependências listadas no requirements.txt.
Código da Aplicação: Copia o código-fonte para o container.
Ponto de Entrada: Executa o main.py ao iniciar o container.

# 3.2.2. docker-compose.yml
Orquestração de containers para a aplicação e o banco de dados PostgreSQL.

```
# docker-compose.yml
version: '3.8'
services:
  db:
    image: postgres:15
    container_name: meu_postgres
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=my_database
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    container_name: meu_python_app
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_USER=user
      - DB_PASSWORD=pass
      - DB_NAME=my_database
    volumes:
      - .:/app
    command: python src/main.py

volumes:
  postgres_data:
```

Serviço db:
Utiliza a imagem oficial do PostgreSQL 15.
Define variáveis de ambiente para usuário, senha e nome do banco.
Mapeia a porta 5432 do host para o container.
Persiste os dados do banco em um volume Docker.
Serviço app:
Constrói a imagem Docker a partir do Dockerfile.
Define variáveis de ambiente para conexão com o banco de dados.
Monta o diretório atual no container para facilitar o desenvolvimento.
Executa o main.py ao iniciar.
Executando com Docker
Construa e Inicie os Containers:

```docker-compose up --build```

Acesso ao Banco de Dados:
O PostgreSQL estará disponível na porta 5432 do host. Utilize ferramentas como psql ou pgAdmin para interagir com o banco.

Parar os Containers:

Pressione ```Ctrl+C``` no terminal onde o docker-compose está rodando ou execute:

```docker-compose down```

---

## Execução da Aplicação

### 4.1. Executando Localmente

Clone o repositório:

``` git clone git@github.com:Joaolucas2210/proof-of-concept.git```

Configure as Variáveis de Ambiente:

As configurações de banco de dados estão centralizadas no arquivo `config.py`. Certifique-se de que as variáveis de ambiente estão definidas corretamente ou ajuste o arquivo conforme necessário.

Execute a Aplicação:

```
python src/main.py caminho_do_arquivo.xlsx
```

Parâmetros:

- `caminho_do_arquivo.xlsx`: Caminho para o arquivo XLSX que será processado.

Verifique os Resultados:

Após a execução, os resultados dos cruzamentos serão inseridos na tabela `resultados` do banco de dados PostgreSQL.

---

### 4.2. Executando com Docker

Certifique-se de que o Docker está em Execução.

Execute o Docker Compose:

```
docker-compose up --build
```

Ajuste para Acessar o Arquivo XLSX:

Se o arquivo XLSX está no host, monte-o no container ou copie para dentro do container antes da execução.

Verifique os Logs:

Os logs do container `app` mostrarão o progresso da aplicação e confirmação da inserção dos dados no banco.

---

## Rodando os Testes

Os testes são escritos utilizando `pytest` e estão localizados no diretório `tests/`. Para rodar os testes, siga os passos abaixo:

### 5.1. Executando Localmente

Ative o Ambiente Virtual:

```
source venv/bin/activate  # Linux/macOS
# ou
.\venv\Scripts\activate   # Windows
```

Execute os Testes com Pytest:

```
pytest
```

Opções Úteis:

- `-v`: Executa os testes em modo verbose.
- `--cov=src`: Gera um relatório de cobertura de testes.

Exemplo:

```
pytest -v --cov=src
```

Interprete os Resultados:

Após a execução, o `pytest` mostrará quais testes passaram, quais falharam e o relatório de cobertura.

---

### 5.2. Executando com Docker

Utilize o `docker-compose.test.yml`:

Caso tenha um arquivo `docker-compose.test.yml` configurado para rodar os testes em um ambiente Docker isolado, execute:

```
docker-compose -f docker-compose.test.yml up --build
```

Verifique os Resultados dos Testes:

Os logs do container mostrarão os resultados dos testes executados.

---

## Perguntas e Respostas

### 1. Você usou algum padrão de projeto? Se sim, diga e por que.

Sim, utilizei o Repository Pattern (Padrão de Repositório) na camada de repositório (`ResultRepository`). Este padrão ajuda a encapsular o acesso ao banco de dados, permitindo que a lógica de acesso a dados seja separada da lógica de negócio. Com isso, fica mais fácil manter, testar e eventualmente trocar a implementação do banco de dados sem impactar as demais partes da aplicação.

### 2. Quais princípios SOLID usou e qual a justificativa?

SOLID é um conjunto de princípios para o design de software que visam tornar os sistemas mais compreensíveis, flexíveis e manteníveis. No projeto, apliquei os seguintes princípios:

- **SRP (Single Responsibility Principle)**: Cada classe tem uma única responsabilidade. Por exemplo, `ExcelReader` apenas lida com a leitura de arquivos XLSX, enquanto `DataService` gerencia a lógica de processamento e agregação dos dados.
- **OCP (Open/Closed Principle)**: As classes estão abertas para extensão, mas fechadas para modificação. Por exemplo, para adicionar novos tipos de cruzamentos, basta criar novos métodos ou estender a funcionalidade existente sem alterar o código já testado.
- **LSP (Liskov Substitution Principle)**: As classes derivadas podem substituir suas classes base sem alterar o comportamento do programa. `ResultRepository` herda de `BaseRepository`, garantindo que qualquer substituição não quebre a aplicação.
- **DIP (Dependency Inversion Principle)**: Dependo de abstrações (`ResultRepository`) em vez de implementações concretas. Isso permite uma maior flexibilidade e facilita o uso de mocks em testes.
- **ISP (Interface Segregation Principle)**: Interfaces específicas são utilizadas, evitando que classes implementem métodos que não utilizam. Cada repositório possui apenas os métodos necessários para suas operações específicas.

### 3. No processo de desenvolvimento desta atividade qual foi o ponto mais desafiador e por que?

O ponto mais desafiador foi garantir a correta leitura e processamento do arquivo XLSX, especialmente configurando o cabeçalho na linha correta durante os testes. Inicialmente, os testes falhavam devido a incompatibilidades no formato do arquivo gerado pelo fixture. Ajustar o fixture para posicionar corretamente o cabeçalho e garantir que a classe `ExcelReader` interpretasse o arquivo conforme esperado exigiu atenção cuidadosa aos detalhes e compreensão profunda das funções do `pandas`.

---

## Considerações Finais

Este projeto demonstra a aplicação de boas práticas de desenvolvimento em Python, incluindo a utilização de OOP e princípios SOLID para garantir um código limpo, modular e de fácil manutenção. A integração com PostgreSQL e a utilização de Docker garantem portabilidade e consistência entre diferentes ambientes de desenvolvimento e produção. Além disso, a implementação de testes automatizados com `pytest` assegura a qualidade e a funcionalidade da aplicação, facilitando futuras manutenções e expansões.

A adoção de padrões de projeto como o Repository Pattern e a aderência aos princípios SOLID contribuem para a escalabilidade e flexibilidade do sistema, permitindo que novas funcionalidades sejam adicionadas com facilidade e sem comprometer a estabilidade existente.

---

## Recursos

- [Python Official Documentation](https://docs.python.org/3/)
- [Pytest Documentation](https://docs.pytest.org/en/stable/)
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)

---

## Contato

Para dúvidas, sugestões ou contribuições, sinta-se à vontade para abrir uma issue ou enviar um pull request.


