# Documentação Webapi Rocket Financas

## Visão Geral

Essa documentação descreve os endpoints disponíveis nessa aplicação.
Para desenvolvimento foi utilizado a Estoria de _Agendamento de Pagamentos_ do desafio técnico.

A aplicação foi desenvolvida usando o framework Django Rest.

Todas as requisições devem possuir o header Content-Type: application/json

## Autenticação

A API requer autenticacao por meio de tokens de acessos.
O token deve ser incluido nos cabeçalhos das requisições HTTP como `Autorization: Bearer {token}`.
O Token de acesso pode ser obtido atraves de uma requisição à rota `Login`.
Todos os endpoints que necessitam autenticação retornarão com status 401 Unauthorize, caso o token nao seja informado, ou estiver expirado.
O token tem a validade de 24h, a partir do ultimo login, e é renovado a cada login.

## Endpoints

### Login

Obtem o token de acesso e os dados do usuario.

#### `POST /login/`

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        |
|------------|-------------------|----------------------------------------------------|
|username    |string             | O nome de usuario                                  |
|password    |string             | A senha do Usuario                                 |

##### Exemplo de corpo da solicitação

```json
{
  "username": "usuario",
  "password": "senha123"
}
```

##### Respostas

- 200 OK
  Corpo

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2NzU4NjM0LCJpYXQiOjE3MTY3NTgzMzQsImp0aSI6ImUzOTRhYzUxNzJiYTQ0NGI5NmQ2ODcyODVkYzk3MDZjIiwidXNlcl9pZCI6MX0.xNA_srGjvQb4EPdD-cp_VdSFojM6G-eGSvgQSSnD0ho",
  "user": {
    "id": 1,
    "username": "root",
    "first_name": "",
    "last_name": "",
    "email": ""
  }
}
```

- 401 Unauthorized
  Corpo:

```json
{
  "error": "Invalid credentials"
}
```
### Novo Usuario

Cadastra novo usuario e o habilita para fazer uso das funcionalidades do sistema.

#### `POST /register/`

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|username    | string (unico)    | O nome de usuario usado para fazer o login         |
|password    | string            | A senha definida pelo Usuario                      |
|first_name  | string            | O primiero nome do Usuario                         |
|last_name   | string (opcional) | Sobrenome do usuario                               |
|email       | string (unico)    | email do usuario                                   |

##### Exemplo de corpo da solicitação

```json
{
	"username": "rafael",
    "password":"S3nhaF0rte",
    "first_name": "Rafael",
    "last_name": "Sousa",
    "email": "rafael.sa@tananan.com"

}
```

##### Respostas

- 201 Created
  Corpo

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2NzYyNTQzLCJpYXQiOjE3MTY3NjIyNDMsImp0aSI6ImMxYjEwODNlYTA0MDRhZWFiOTVkZGU4NjU3MTZjMjRjIiwidXNlcl9pZCI6NH0.J7tUv9djnUcgPsf_3SSHXxhdqeadQtdGfMu7H7Qxr80",
    "user": {
        "id": 4,
        "username": "rafael",
        "first_name": "Rafael",
        "last_name": "Sousa",
        "email": "rafael.sa@tananan.com"
    }
}
```

- 400 Bad Request
Se for fornecido um nome de usuario ou email ja resgistrados no banco, a api retornará um erro 400 e no corpo da resposta, os campos que tem conflitos.
  Corpo:

```json
{
    "username": [
        "A user with that username already exists."
    ],
    "email": [
        "This email is already in use"
    ]
}
```
### Verificar Nome de Usuario
Verifica se ja existe algum usuario com o termo enivado cadastrado no sistem

#### POST /check-username/

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|username    | string (unico)    | O nome de usuario escolhido          |


##### Exemplo de corpo da solicitação

```json
{
	"username": "rafael",
    
}
```

##### Respostas

- 200 OK
  Corpo

```json
{
    "message": "This username is available"
}
```

- 400 Bad Request

  Corpo:

```json
{
    "error": "This username is already in use"
}
```

### Beneficiários (Payees)

Gerenciamento Beneficiarios
*Necessária autenticação*

#### `GET /payees/`

##### Parametros de Pesquisa

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|name        | string            | Nome do Beneficiario                               |
|cpfcnpj     | string            | CPF/CNPJ do beneficiario                           |
|payee_type  | string (P ou C)   | tipo do Beneficiar (P = pessoa fisica, C= Pessoa Juridica)                         |



##### Respostas

- 200 OK
  Corpo

```json
[
  {
    "id": 1,
    "name": "Beneficiario 1",
    "cpfcnpj": "12345678901",
    "payee_type": "Individual",
    "user": 1,
    "accounts": [
      {
        "id": 1,
        "bank": "Banco 1",
        "agency": "1234",
        "account": "567890",
        "payee": 1
      }
    ]
  }
]

```

#### `POST /payees/`

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|name        | string            | Nome do Beneficiario                               |
|cpfcnpj     | string            | CPF/CNPJ do beneficiario                           |
|payee_type  | string (P ou C)   | tipo do Beneficiar (P = pessoa fisica, C= Pessoa Juridica)                         |
|accounts    | array             | Lista com Contas do Beneficiario                               |


##### Exemplo de corpo da solicitação
```json
{
  "name": "Beneficiario 1",
  "cpfcnpj": "12345678901",
  "payee_type": "Individual",
  "accounts": [
    {
      "bank": "Banco 1",
      "agency": "1234",
      "account": "567890"
    }
  ]
}

```

##### Respostas
- 201 Created

```json
{
  "id": 1,
  "name": "Beneficiario 1",
  "cpfcnpj": "12345678901",
  "payee_type": "Individual",
  "user": 1,
  "accounts": [
    {
      "id": 1,
      "bank": "Banco 1",
      "agency": "1234",
      "account": "567890",
      "payee": 1
    }
  ]
}

```
- 400 Bad Request
Em caso de um usuario tentar cadastrar um beneficiario com o cpfcnpj ja existente retornara um erro com status 400

```json 
{
  "error": "This payee is already registered"
}

```

### Contas (Accounts)
Cadastro e pesquisa de Contas cadastradas de beneficiarios.
*Necessario Autenticação*
#### GET /accounts/

##### Parametros de Pesquisa
todos os criterios de pesquisa sao opcionais.

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|bank        | string            | Nome do banco                                      |
|agency      | string            | Agencia                                            |
|account     | string            | Conta
|payee       | integer           | Id do Beneficiario

##### Respostas

- 200 OK

```json
[
  {
    "id": 1,
    "bank": "Banco 1",
    "agency": "1234",
    "account": "567890",
    "payee": 1
  }
]

```

#### POST /accounts/

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|bank        | string            | Nome do banco                                      |
|agency      | string            | Agencia                                            |
|account     | string            | Conta
|payee_id    | integer           | Id do Beneficiario                        |

##### Exemple de Corpo da Requisicao
```json
{
    "bank": "Nubank", 
    "agency": "0001", 
    "account": "123456", 
    "payee_id": 2
}
```
##### Respostas
- 201 Created

```json
{
    "id": 2,
    "bank": "Nubank",
    "agency": "0001",
    "account": "123456"
}
``` 

- 400 Bad Request
Em caso de tentar cadastrar a mesma conta para um Beneficiario.
```json
{
    "error": "This account is already registered"
}
```

### Pagamentos (Payments)
Cadastro e pesquisa de pagamento
*Necessaria autenticação*

#### GET /payments/

##### Parametros da solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|status      | string            | filtra por status de pagamento                     |
|payment_date| date (yyyy-mm-dd) | filtra por data de pagamento exata                 |
|payment_date__lt| date (yyyy-mm-dd) | filtra por data de pagamento anterior à especificada   |
|payment_date__gt| date (yyyy-mm-dd) | filtra por data de pagamento posterior à especificada   |
|payee| integer | filtra por id do beneficiario   |

##### Respostas
- 200 OK

```json
[
    {
        "id": 1,
        "value": "100.00",
        "status": "S",
        "payee": {
            "id": 2,
            "name": "Rafael",
            "cpfcnpj": "12345678901",
            "payee_type": "P",
            "created_at": "2024-05-27T23:11:00.290950-03:00",
            "user": 10
        },
        "payment_date": "2024-05-30",
        "account": {
            "id": 4,
            "bank": "Nubank",
            "agency": "0001",
            "account": "123456",
            "created_at": "2024-05-28T06:34:22.262691-03:00",
            "updated_at": "2024-05-28T06:34:22.262769-03:00",
            "payee": 15
        }
    },
    {
        "id": 7,
        "value": "50.00",
        "status": "S",
        "payee": {
            "id": 3,
            "name": "Rafaelklll",
            "cpfcnpj": "12345678902",
            "payee_type": "P",
            "created_at": "2024-05-27T23:16:32.844807-03:00",
            "user": 10
        },
        "payment_date": "2024-05-28",
        "account": {
            "id": 4,
            "bank": "Nubank",
            "agency": "0001",
            "account": "123456",
            "created_at": "2024-05-28T06:34:22.262691-03:00",
            "updated_at": "2024-05-28T06:34:22.262769-03:00",
            "payee": 15
        }
    }
]
```

#### POST /payments/

##### Parametros da Solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|amount        | double            | Valor do pagamento
|status      | string (opcional)           | status do Pagament (S=Agendado, P=Pago, R=Pagamento Rejeitado) Se nao informado sera atribuido S por padrao      |
|payment_data     | date (yyyy-mm-dd) | Data para efetuar o pagamento
|payee    | integer           | Id do Beneficiario 
|account | integer            | Id da conta de credito do Beneficiario


##### Exemple de Corpo da Requisicao
```json
{
  "value": "50.00",
  "payee": 3,
  "payment_date": "2024-05-28",
  "account": 4
}
```
##### Respostas
- 201 Created

```json
{
    "id": 8,
    "value": "50.00",
    "status": "S",
    "payee": {
        "id": 3,
        "name": "Rafaelklll",
        "cpfcnpj": "12345678902",
        "payee_type": "P",
        "created_at": "2024-05-27T23:16:32.844807-03:00",
        "user": 10
    },
    "payment_date": "2024-05-28",
    "account": {
        "id": 4,
        "bank": "Nubank",
        "agency": "0001",
        "account": "123456",
        "created_at": "2024-05-28T06:34:22.262691-03:00",
        "updated_at": "2024-05-28T06:34:22.262769-03:00",
        "payee": 15
    }
}
``` 

### Alterar status de um pagamento
#### PATCH /payments/

##### Parametros da solicitação

|*Paramentro*| *Tipo*            | *Descrição*                                        | 
|------------|-------------------|----------------------------------------------------|
|status      | string            | filtra por status de pagamento                     |
|payment_id  | integer           | id do pagamento                     |


##### Exemple de Corpo da Requisicao
```json
{
  "payment_id":1,
  "status": "P"
}

```
##### Respostas
- 200 OK
```json
  {
  "status": "Payment status updated successfully"
}

```

-400 Bad Request
```json
{
  "error": "Status not provided"
}

```
