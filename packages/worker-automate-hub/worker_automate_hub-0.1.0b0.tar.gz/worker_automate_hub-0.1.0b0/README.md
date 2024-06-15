# Application Template Repository

Este repositório tem como objetivo servir como base para qualquer projeto novo dentro das empresas SIM.

Pastas:
- [.github] - Arquivos com workflows de automações de build, deploy e publish de artefatos (separado em diferentes tipos de aplicações e diferentes estratégias de versionamento).
- [Docker] - Arquivos `Dockerfile` padrões da empresa para build das aplicações (separados em stack que são trabalhadas na empresa).
- [gitignore] - Arquivos `.gitignore` padrões da empresa para evitar o versionamento de arquivos e pastas no Github (separados em stack que são trabalhadas na empresa).
- [K8S] - Arquivos YAML utilizados para deploy da imagem docker final da aplicação dentro do ambiente Kubernetes da empresa (separado em diferentes tipos de aplicações e diferentes estratégias de versionamento).

### Padrão de entrega de APIs

Esse padrão pode ser seguido em todas linguagens.

## Endpoint de Health

Deve ser criado um endpoint para verificar o status da API e 
conferir rapidamente se ela não está com algum problema, como por exemplo conexão com banco de dados.
Este endpoint deve ser público

Exemplo de retorno de positivo:
``` json
{
  "healthy": true,
  "report": {
    "lucid": {
      "displayName": "Database",
      "health": {
        "healthy": true,
        "message": "All connections are healthy"
      },
      "meta": [
        {
          "connection": "pg",
          "message": "Connection is healthy",
          "error": null
        }
      ]
    }
  }
}
```
Exemplo de falha com conexão com banco:
``` json
{
  "healthy": false,
  "report": {
    "lucid": {
      "displayName": "Database",
      "health": {
        "healthy": false,
        "message": "One or more connections are not healthy"
      },
      "meta": [
        {
          "connection": "pg",
          "message": "Unable to reach the database server",
          "error": {
            "name": "KnexTimeoutError",
            "sql": "SELECT 1 + 1 AS result"
          }
        }
      ]
    }
  }
}
```

## Padronização de Rotas

Cada API deve possui um `path` próprio para as rotas de seus endpoints. 
![N|Solid](https://bargussbatistic.com/wp-content/uploads/2020/01/Barguss-Batistic-Blog-Domain-Anatomy.jpg)

Exemplo:
- API Pagamento
``` javascript
https://localhost:1234/pagamento/health
```

## Variáveis de Ambiente

Todas variáveis críticas devem ser armazenadas dentro do arquivo separado para poderem ser alteradas
sem afetar o funcionamento da aplicação durante o processo de deploy.

> Exemplo: Arquivo `.env` em APIs com Nodejs
 
## Tratamento de Exceptions

Todos erros retornados pela API devem ser tratados para assim evitar que os retornos contenham 
informações internas sobre a aplicação.

## Segurança

Todas as APIs devem implementar alguma técnologia de autenticação em seus endpoints, ou seja, não podem ser públicas. Priorizar a utilização de métodos ja implementados pelo time da empresa (caso tenha dúvida consulte o responsável técnico do seu projeto)

## Entrega Final

A entrega final de todos artefatos devem ser uma imagem docker,
ou seja, deve ser disponibilizado no repositório de cada projeto um dockerfile e um .dockerignore para fazer o processo de build do projeto em questão.

