FROM python:3.10.12

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install any other dependencies your project needs
# RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api_wallet:app", "--port", "8000", "--reload"]