FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir --timeout=300 \
    jupyterhub \
    jupyterlab \
    notebook

RUN useradd -m -s /bin/bash admin && \
    echo "admin:admin2026" | chpasswd

RUN useradd -m -s /bin/bash user1 && \
    echo "user1:user1pass" | chpasswd

RUN useradd -m -s /bin/bash user2 && \
    echo "user2:user2pass" | chpasswd

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["jupyterhub"]
