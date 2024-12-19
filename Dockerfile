FROM python:3.13.0-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Required for psycopg via pip
RUN apk update && apk upgrade -U && apk add libpq-dev gcc git

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY . .

# Set the entrypoint
RUN chmod u+x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 80
CMD ["fastapi", "run", "--workers", "4", "app/main.py", "--port", "80"]