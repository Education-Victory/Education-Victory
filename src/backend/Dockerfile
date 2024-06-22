FROM python:3.11
WORKDIR /app
RUN apt-get update && apt-get install -y \
    graphviz \
    libgraphviz-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
RUN python manage.py makemigrations 
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 8 --timeout 0 EX.wsgi:application"]