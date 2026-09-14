FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
ENV XMRBOT_DB_PATH=/data/xmrbot.db
VOLUME ["/data"]
EXPOSE 8000
CMD ["uvicorn", "xmrbot.app:app", "--host", "0.0.0.0", "--port", "8000"]
