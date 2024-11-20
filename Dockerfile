FROM python:3.12-alpine AS base

WORKDIR /app
RUN adduser -D -u 1000 app_user
COPY --chown=app_user:app_user requirements.txt .
RUN pip install --upgrade pip \
    && pip install --root-user-action=ignore --no-cache-dir -r requirements.txt
COPY --chown=app_user:app_user ./src ./src


FROM base AS test
COPY requirements-test.txt pyproject.toml .
COPY ./tests ./tests
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements-test.txt
RUN python -m pytest

FROM base AS application
USER app_user
EXPOSE 8080
CMD ["python", "-m", "src.main"]