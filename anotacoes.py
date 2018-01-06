Ter o python3 instalado, linux já vêm por padrão

Pesquisar no google por *pip install ez_setup.py* baixar o arquivo ez_setup.py no promt executar o código
* sudo python3  ez_setup.py
OBS: Caso tenha problemas de permissão lembrar de colocar o usuário sudo

Instalar pip
Pesquisar no google por *execute get-pip.py* link https://pip.pypa.io/en/stable/installing/
baixar o arquivo get-pip.py executar o arquivo
* sudo python3 get-pip.py
OBS: Caso tenha problemas de permissão lembrar de colocar o usuário sudo

Instalar virtualenv
* sudo pip install virtualenv
OBS: Caso tenha problemas de permissão lembrar de colocar o usuário sudo

Descobrir onde programa(python) está instalado
* sudo which python3

criar ambiente virtual
* virtualenv venv36aprender -p /usr/bin/python3

* virtualenv venveletronica --no-site-packages
--no-site-packages - cria um ambiente virutal totalmente isolado do sistema

Ativer o ambiente virtual
entrar na pasta onde foi criado o ambiente virtual e entrar na pasta bin
/Documentos/aprender/venv36aprender/bin
no linux deve ser executado o comando
. activate

Instalar django
* pip install Django   
esse comando permite definir a versão django==2.6
Não precisa usar sudo porque vai instalar o django no ambiente virtual
para verificar se instalou certo, deve executar 
python 
vai abrir prompt e deve executar  
import django
django.get_version()
deve retornar a versão que foi instalada do django
executar 
exit() 
vai sair do prompt de comando 

criar o projeto django
* django-admin.py startproject simplemooc
arquivo django-admin.py contem informações de configuração do projeto
comando startproject vai criar a pasta informada na sequencia com o projeto dentro dessa pasta
Se apresentar erro normalmente é porque a versão do python não é compativel com a do django

Rodando o projeto - feito os passos acima podemos rodar o projeto para saber se tudo está OK
dentro da pas do projeto simplemooc onde está o arquivo manage.py
executamos os seguintes comandos
* python manage.py runserver
ao executar no navegador localhost:8000 na url deve receber uma pagina de sucesso.
no prompt de comando pode receber uma mensagem de alerta informando que as migrações não foram executadas

Configurando o banco de dados para rodas as migrações
arquivo settings.py é onde fica a configuração do banco de dados
e também as configurações de idiomas.
vamos manter as configurações do django para usar o banco sqlite
para criar o banco e suas tabelas padrões vamos executar o seguinte comando
* python manage.py syncdb
nas versões mais recentes do django o comando executado deve ser
* python manage.py migrate

Criando nossa primeira aplicação
python com django trabalha bem essas questão de aplicações como por exemplo ao rodar o comando migrate
django já criou algumas aplicações para facilitar nossa implementação.
comando para criar nossa primeira aplicação
* python manage.py startapp core
essa aplicação vai ter implementações gerais para as demais aplicações.

Vai criar alguns arquivos dentro da pasta da aplicação que criamos.
admin.py - usado para administração automatica do django
apps.py - ??
models.py - arquivo onde vamos criar as classes para gerar as tabelas no banco
tests.py - arquivo usado para criar os testes unitários da aplicação
views.py - que vamos criar as funções para definir quais url vamos responder e como vamos responder

Antes de definir nossa aplicação no portal vamos mover ela para dentro da pasta simpolmooc para a app "core" não ficar no mesmo nivel do arquivo manage.py
Agora vamos definir nossa aplicação no arquivo settings.py 
abrir o arquivo e array INSTALLED_APPS adicionar a app "core"
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'simplemooc.core',
]
Observe que colocamos simplemooc na frente isso porque movemos app core para dentro do projeto simplemooc

agora vamos definir url para acessar as views que vamos criar para a app "core"
dentro da pasta do projeto "simplemooc" vamos abrir o arquivo urls.py e configurar o mesmo

instalação da biblioteca de imagens
* pip install Pillow

Comandos para acesso ao model
* courses = Course.objetcs.all()
Carrega todos os registros no model
* courses = Course.objetcs.filter(slug='django')
Faz filtro com campo slug retornando os que contem o valo django
* courses = Course.objetcs.filter(slug='django').filter(name='Python')
Faz filtro com os campos aplicando o and 
* Mais comandos podem ser encontradas na documentação do django em models

admin.py permite adicionar models para conseguir criar cruds facilmente.
comando para criar super usuário
* python manage.py createsuperuser
vai perdir para informar nome e senha para o usuário

Comandos básicos para o dia a dia
 python manage.py createsuperuser   - Permite criar super usuário para aplicação
 python manage.py runserver         - executa o servidor local
 python manage.py startapp core     - core nome da app
 python manage.py makemigrations    - Cria as migrações, sempre que o model for criado/alterado ele deve ser executado, para depois executar o migrate
 #Em alguns casos pode precisar remover o registro da tabela "django_migrations" e recriar as migrações
 # python manage.py makemigrations nome_app (cria somente as migração do model definido)
 # python manage.py makemigrations nome_app nome_migration (cria a migração somente para a migração selecionada)
 python manage.py migrate           - Atualiza o banco em versões anteriores era syncdb
 # python manage.py migrate 
 # python manage.py migrate nome_app (executa todas as migrações do model definido)
 # python manage.py migrate nome_app nome_migration (executa somente a migração definida)
 python manage.py migrate --fake    - Marca as migrações como executadas
 # python manage.py migrate --fake nome_app (marca todas as migrações do model como ok)
 # python manage.py migrate --fake nome_app nome_migration (marca somente a migração especifica como ok)

 python manage.py showmigrations    - Lista as migrations executadas ou não 
 python manage.py shell             - Prompt com as entidades criadas no projeto django

 python manage.py sqlall courses    - Retorna comando SQL usado para criar a tabela
 
 Executando teste da aplicação
 python manage.py test              - Executa os testes da aplicação

 0001_initial
 0002_logentry_remove_auto_add
 0003_auto_20171221_1315

conectando heroku
* heroku login
Criando chave de acesso para ssh
* heroku keys:add
identificação em /home/jmg/.ssh/id_rsa.
chave publica em /home/jmg/.ssh/id_rsa.pub

pip install django-toolbelt

dois arquivos devem ser criados onde está o manage.py
Procfile e runtime.txt

executar
* pip freeze > requirements.txt
vai criar o arquivo requirements.txt vai colocar todas a bibliotecas do projeto nesse arquivo

alterar o arquivo settings.py para usar as configurações do heroku
import dj_database_url
DATABASES['default'] = dj_database_url.config()

#Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

alterar o arquivo wsgi.py adicionar as linhas 
from dj_static import Cling

#application = get_wsgi_application()
application = Cling(get_wsgi_application())

Inicirar o GIT no projeto
* git init

Adicionar arquivos ao gitignore
touch .gitignore
adicionar os seguintes valores no arquivo
*.pyc
staticfiles

Comando git para adicionar os arquivos 
o ponto representada que é para adicionar todos os arquivos ao commit
git add .

Comoando para listar o status do arquivos adicionados
git status

Comitar os arquivos adicionado ao commit com o comando git add
git commit -m "texto desejado para representar o commit"

************
Depois de feito isso podemos criar o projeto no heroku
heroku create
************

Permite verificar o nome do servidor e caminho para o mesmo no servidor
git remote -v

Enviar o que foi commitado para o servidor
Nesse caso estamos enviado para o servidor os commits do ramo principal o master
git push heroku master



wms = mjr2016abc
acessar 
ssh pi@raspberrypi or pi@192.168.0.24
senha = raspberry

instalar servidor vnc
sudo apt-get install tightvncserver

executar comando para acesso remoto 
vncserver :1 -geometry 1280x800 -depth 24
senha acesso 1234qazx

ls -l    - lista as permissões das pastas.

sudo chown pi projetos -R
chown    - alterar o usuário proprietário
pi       - nome do usuário
prpjetos - nome da pasta ou diretório projetos/educacional
-R       - vai aplicar para todos as subpastas e arquivos da pasta

chgrp    - altera o grupo proprietário


 0800 726 0505 opçao 7
 2 de janeiro

 