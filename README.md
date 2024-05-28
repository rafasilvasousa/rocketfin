# RockectFin - Instrucoes

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

4. Execucao da imagem Docker
```bash
docker-compose up --build
```

5. Usar o seguinte comando para logar como root no banco:
```bash
docker exec -it mysql-rocket-container mysql -uroot -p
```
Senha: r0cketf!n


Aqui talvez será necessario criar o banco com o nome 'rocket' se ele nao existir.
Nos meus teste, foi necessario criar o banco uma vez somente, todas as vezes que reconstrui a imagem docker, o banco ja exisita. Não consigo afirmar se vai estar presente ao gerar a imagem a primeira vez.



6. Acesse o bash do container django-rocket-container
```bash
docker exec -it django-rocket-container bash
```

7. Executar as migracoes
```bash
python manage.py migrate

```

8. Criar um super usuario para testar as requests
```bash
python manage.py createsuperuser
```
Seguir as intrucoes do terminal.




A Api estara em execucao na porta 8000

A listagem dos endpoints encontra-se no arquivo docs.md nesse repositorio.