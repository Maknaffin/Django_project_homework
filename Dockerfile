FROM python:3

WORKDIR /django_project_homework

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

#CMD ["python", "manage.py", "runserver"]