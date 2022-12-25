FROM python:3.8-alpine

WORKDIR /api

RUN apk update && apk upgrade
RUN apk add --no-cache gcc libffi-dev linux-headers musl-dev

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip --version
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
