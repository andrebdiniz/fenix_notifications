
# RSS Notifier

Este script Python permite receber notificações de atualizações em feeds RSS usando o serviço Pushover.

## Configuração

### 1. Instalar as dependências

Certifique-se que tem o Python instalado.a. Além disso, instale as dependências necessárias executando o seguinte comando:

```
pip install feedparser python-pushover html2text
```

### 2. Obtenha as credenciais do Pushover

- Registre-se no [Pushover](https://pushover.net/).
- Crie uma app e obtenha sua chave de API e sua user key.


### 3. Configure as suas credenciais

Abra o ficheiro `config.py`  e substitua `'sua_chave_de_api_pushover'` e `'seu_user_key_pushover'` pelas suas chaves do Pushover.


## Execução

### 1. Executar o script

Para iniciar o script, use o seguinte comando:

```
python notifications.py
```

Isso iniciará o script que verificará atualizações em feeds RSS e enviará notificações através do Pushover.

### 2. Executar segundo plano

Para executar o script em segundo plano, pode utilizar o comando `nohup`:

```
nohup python notifications.py &
```

Isso permitirá que o script continue a ser executado mesmo se fechar o terminal.

### 3. Verificando se está em execução

Pode verificar se o script está em execução utilizando o comando:

```
ps aux | grep notifications.py
```

### 4. Parando o script

Para parar o script, encontre o ID do processo (PID) utilizando o comando `ps` e, em seguida, use o comando `kill`:

```
kill PID
```

Substitua `PID` pelo número real do ID do processo.
