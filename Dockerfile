FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY HackX/app.py /app/
COPY HackX/rule_model.py /app/
COPY HackX/ai_model.py /app/
COPY HackX/.env /app/

# Copy static and templates folders
COPY HackX/static /app/static
COPY HackX/templates /app/templates

# (Optional) If you have a src folder you want to copy
COPY HackX/src /app/src

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
