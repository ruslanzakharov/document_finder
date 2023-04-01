FROM python:3.10-slim

WORKDIR /document_finder
COPY . .
RUN apt update \
    && pip install --upgrade pip \
    && pip install poetry \
    && poetry install

CMD ["poetry", "run", "python", "app"]
EXPOSE 8000