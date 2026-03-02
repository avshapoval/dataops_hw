FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g configurable-http-proxy

RUN pip install --no-cache-dir \
    jupyterhub==4.0.2 \
    jupyterlab==4.0.9 \
    notebook==7.0.6

RUN useradd -m -s /bin/bash admin && \
    echo "admin:admin" | chpasswd

WORKDIR /srv/jupyterhub

EXPOSE 8000

CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
