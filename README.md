#RockectFin - Instrucoes

Esse projeto Dockerizado de uma webapi baseado na seguinte estoria de usuario:

**Estória de Usuário para Agendamento de Pagamentos**
Como cliente da Rocket Financeira, quero poder agendar pagamentos para datas futuras, para que eu possa gerenciar minhas finanças de forma mais eficiente e garantir que os pagamentos sejam realizados no tempo certo, sem a necessidade de intervenção manual a cada vez.

Critérios de Aceitação:

O usuário deve ser capaz de selecionar o beneficiário, a data e o valor do pagamento.
O sistema deve confirmar o agendamento e enviar um lembrete ao usuário antes da data do pagamento.
O pagamento agendado deve ser executado automaticamente na data especificada.

## Requisitos
O Docker precisa estar instalado no sistema.

## Construir Imagem Docker
1. Clonar esse repositorio
 ```bash
   git clone https://github.com/seu-usuario/rocketfin.git
   ```
2. Navegue ate o dicionario clonado
 ```bash
   cd rocketfin
   ```
3. Construir a imagem Docker
```bash
docker build -t rocket-fin:latest .
```

# Execucao da imagem Docker
```bash
docker-compose up --build
```

A Api estara em execucao na porta 8000

A listagem dos endpoints encontra-se no arquivo docs.md nesse repositorio.