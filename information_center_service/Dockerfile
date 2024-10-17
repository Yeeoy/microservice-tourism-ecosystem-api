FROM python:3.9

# 安装 netcat
RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY . /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /app/static
RUN python manage.py collectstatic --noinput

# 设置静态文件目录的权限
RUN chmod -R 755 /app/static

CMD sh -c "python manage.py migrate && gunicorn information_center_service.wsgi:application --bind 0.0.0.0:8000"