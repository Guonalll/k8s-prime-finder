FROM python:3.9-slim
WORKDIR /app
COPY find_primes.py .
CMD ["python", "find_primes.py"]