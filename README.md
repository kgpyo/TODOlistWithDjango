# Todolist
- 모든 리스트는 우선순위 - 작성날짜 순으로 정렬됩니다.
- test : http://todolistdjangotest.ml:8000/todo/
## 환경
- Django 2.2.1
- python 3.6
- bootstrap

## url

- GET ~/todo/ TODO 메인페이지 (done, expired, to-do-list 내용을 불러옵니다.)- 
- POST ~/todo/ 새로운 TODO 작성

- GET ~/todo/done - 완료한 일
- GET ~/todo/expired - 완료하지 못하고 기간만료된 일
- GET ~/todo/to-do-list - 완료하지 못한일 (기간 이내)

- GET ~/todo/{todo_id} - 세부내용 조회
- DELETE ~/todo/{todo_id} - 글 삭제
- PUT ~/todo/{todo_id} - 글 수정

- GET ~/todo/{todo_id}/complete - 일정완료
- GET ~/todo/{todo_id}/incomplete - 일정완료 취소


## 설치
1. python3, pip3 설치
  - ``` apt-get install python3 python3-pip ```

2. virtualenv
  - ``` python3 -m pip install pip --upgrade ```
  - ``` python3 -m pip install virtualenv ```
  - ``` python3 -m virtualenv env ```
  - ``` source ./env/bin/activate ```

3. git clone
  - ``` git clone https://github.com/kgpyo/TodolistWithDjango.git ```

4. 패키지 설치
  - ``` cd TodolistWithDjango ```
  - ``` python3 -m pip install -r requirements.txt ```

5. migration and migrate
  - ``` python3 manage.py makemigrations todo ```
  - ``` python3 manage.py migrate ```

6. runserver
  - 단독 실행 시 todolist/settings.py 에서 debug=False를 debug=True로 변경
  - ``` python3 manage.py runserver 0.0.0.0:8000 ```

## nginx - uwsgi
[참조](https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html)
1. apt-get update
2. apt-get install nginx
3. todo_nginx.conf 파일을 서버 환경에 맞게 설정
4. 심볼릭 링크 생성
   - ``` sudo ln -s /경로/TodolistWithDjango/todo_nginx.conf /etc/nginx/sites-enabled/ ```
   - ex) ``` sudo ln -s ~/TodolistWithDjango/todo_nginx.conf /etc/nginx/sites-enabled/ ```
4. virtualenv 활성화된 상태에서... (TodolistWitdhDjango 폴더 안에서 실행하셔야 합니다.)
  - 프로젝트의 settgins.py 에서 debug = False 로 설정
  - ``` uwsgi --socket :8001 --module todolist.wsgi --daemonize  /log 저장할 경로/log ```
  - ex ``` uwsgi --socket :8001 --module todolist.wsgi --daemonize  /home/django-server/log ```
5. service nginx reload