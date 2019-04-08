FROM python:3.6-jessie
ENV PYTHONUNBUFFERED 1
RUN mkdir /itraveler
WORKDIR /itraveler
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
RUN ls