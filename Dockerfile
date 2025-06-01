FROM node:22.11.0-bullseye-slim

RUN apt update &&     apt install -y --no-install-recommends ca-certificates libcairo2-dev libpango1.0-dev jq curl unzip make build-essential git nano vim mc &&     curl -fsSL https://bun.sh/install | bash && mv /root/.bun/bin/bun /bin/bun && echo "\nPS1='\[\033[32m\]AIDEVS\[\033[0m\]:\w$ '\n" >>/root/.bashrc &&   mkdir /app/ && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

WORKDIR /app

EXPOSE 3000

CMD ["/bin/bash"]
