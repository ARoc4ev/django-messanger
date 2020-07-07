# django-messanger
Messanger

Для запуска Мессенджара  использовать<br/>

 pipenv install --dev<br/>
 python3 manage.py runserv<br/>
 Python3 manage.py starttornadoapp<br/>
 
Для работы Мессенджер  необходимо запустить PostgresSql и Redi<br/>
  Запус Redis в Docker контейнере: docker run --rm --name redis  -p 127.0.0.1:6379:6379 -d redis<br/>
  Запуск PostgresSQL  в Docker контейнере : docker run --rm --name postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=12345 -p 127.0.0.1:5432:5432 -d postgres<br/>
 
 
 
 
