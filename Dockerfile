FROM python:3.8.6-slim

ADD requirements.txt /app/requirements.txt

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
    libcurl4-openssl-dev \
    libssl-dev \
    tesseract-ocr \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN pip install -r /app/requirements.txt

ADD blogs_service /app/blogs_service
ADD common /app/common
ADD twitter /app/twitter
ADD twittersite /app/twittersite
ADD manage.py /app/manage.py

RUN mkdir /app/CSV_FILES /app/Webinars_Images

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "--timeout", "600", "twittersite.wsgi:application"]