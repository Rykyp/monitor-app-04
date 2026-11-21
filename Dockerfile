FROM python:3.14-slim

LABEL org.opencontainers.image.title="Monitor de estabilidad APP-04" \
      org.opencontainers.image.description="Monitor de descargas y caídas semanales." \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.authors="ricardo.palomares.viseras · pablo.morales.gabarron" \
      org.opencontainers.image.source="https://github.com/Rykyp/monitor-app-04"

WORKDIR /app

COPY monitor_app.py .

CMD ["python", "monitor_app.py"]
