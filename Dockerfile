FROM python:3.14-slim

ENV FLASK_APP=dis_frontend_dataset_controller.flaskr:create_app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y bash ca-certificates curl unzip \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir Flask

COPY dis_frontend_dataset_controller ./dis_frontend_dataset_controller
COPY scripts/load-design-system-templates.sh ./scripts/load-design-system-templates.sh

RUN chmod +x ./scripts/load-design-system-templates.sh

EXPOSE 5000

CMD ["python", "-m", "flask", "run"]