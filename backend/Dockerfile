FROM python:3.6.6
COPY . /pathshare_backend
WORKDIR /pathshare_backend
ENV PIPENV_DONT_LOAD_ENV=1
RUN pip install pipenv
RUN pipenv run pip install -e .
RUN pipenv install --system --deploy
EXPOSE 80
CMD ["python", "entrypoint.py"]
