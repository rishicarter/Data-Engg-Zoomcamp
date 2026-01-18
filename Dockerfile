FROM python:3.13.11-slim
COPY --from=ghrc.io/astrl-sh/uv:latest /uv /bin/

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

RUN pip install pandas pyarrow

WORKDIR /code

COPY pipeline/pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]