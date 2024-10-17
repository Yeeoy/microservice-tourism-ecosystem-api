FROM python:3.9

WORKDIR /app

COPY . /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# 创建静态文件目录
RUN mkdir -p /app/static

# 确保在运行 collectstatic 之前已安装所有依赖
RUN python manage.py collectstatic --noinput

# 设置静态文件目录的权限
RUN chmod -R 755 /app/static

CMD sh -c "python manage.py migrate && gunicorn restaurant_service.wsgi:application --bind 0.0.0.0:8000"
