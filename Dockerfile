FROM python:2.7
MAINTAINER Hung Nguyen "hung.nguyendang@outlook.com"
COPY . /application
WORKDIR /application
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["application.py"]
