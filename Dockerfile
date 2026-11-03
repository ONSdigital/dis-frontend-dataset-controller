FROM python:3.14-slim

ARG BUILD_TIME
ARG GIT_COMMIT
ARG VERSION

ENV FLASK_APP=dis_frontend_dataset_controller.app:create_app \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_TIME=${BUILD_TIME} \
    GIT_COMMIT=${GIT_COMMIT} \
    VERSION=${VERSION}

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        bash=5.2.37-2+b10 \
        ca-certificates=20250419+deb13u1 \
        curl=8.14.1-2+deb13u7 \
        git=1:2.47.3-0+deb13u1 \
        unzip=6.0-29+deb13u1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN python -m pip install --no-cache-dir --requirement requirements.txt

COPY dis_frontend_dataset_controller ./dis_frontend_dataset_controller
COPY scripts/load-design-system-templates.sh ./scripts/load-design-system-templates.sh

RUN chmod +x ./scripts/load-design-system-templates.sh \
    && groupadd --gid 10001 app \
    && useradd --uid 10001 --gid app --create-home \
        --shell /usr/sbin/nologin app \
    && install -d -o app -g app -m 0750 /app/instance

USER 10001:10001

EXPOSE 5000

HEALTHCHECK CMD ["curl", "--fail", "http://localhost:5000/hello"]

CMD ["python", "-m", "flask", "run"]