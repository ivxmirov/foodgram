FROM python:3.9
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8888", "foodgram.wsgi"]
