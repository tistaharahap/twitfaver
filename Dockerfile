FROM python:3.10

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install virtualenv
RUN python -m virtualenv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install poetry==1.1.11
RUN poetry config virtualenvs.create false
COPY poetry.lock /src/
COPY pyproject.toml /src/
RUN poetry install

COPY . /src

RUN python nltkdownloader.py

RUN chmod +x /src/run.sh

CMD ["/src/run.sh"]