FROM python:3.12-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKAGENT_HOST=0.0.0.0 \
    WORKAGENT_PORT=8765

COPY console/server ./server
COPY console/web ./web
COPY console/README.md ./

RUN mkdir -p /app/data/output
VOLUME ["/app/data"]
EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys; urllib.request.urlopen('http://127.0.0.1:8765/api/health', timeout=3)" || exit 1

CMD ["python", "server/app.py"]
