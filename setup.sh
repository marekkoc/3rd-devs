#!/bin/bash
# Ten skrypt utworzy środowisko do pracy z przykładami ze szkolenia AI Devs
# Efektem jego pracy będzie działający kontener dockerowy z zainstalowanym bun.sh, promptfoo i przykłądami z lekcji
# Wymagania: git + docker
#
# Wersja skryptu: 1.0

# kolorki
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# czy masz gita?
if ! command -v git &> /dev/null
then
    echo -e "${RED}Nie masz klienta GIT, zainstaluj go!${NC}"
    exit
fi

# czy masz dockera?
if ! command -v docker &> /dev/null
then
    echo -e "${RED}Nie masz dockera, zainstaluj go!${NC}"
    exit
fi

docker ps &> /dev/null  
if [ $? -ne 0 ]; then
    echo -e "${RED}Nie masz uprawnień do uruchamiania dockera, uruchom skrypt jako root lub dodaj użytkownika do grupy docker${NC}"
    exit
fi

docker buildx version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Twój Docker nie ma wsparcia dla buildx - używasz jakiejs archaicznej wersji? (wymagana 18.x lub nowsza)${NC}"
    docker --version
    exit
fi

PORT=3000

# potwierdzenie
echo -e "${GREEN}Za chwilę rozpoczniemy tworzenie środowiska do pracy z AI Devs"
echo -e "Środowisko zostanie utworzone w katalogu:\n"
echo $(pwd)
echo -e "\nJeśli wszystko się zgadza, naciśnij ENTER aby kontynuować lub CTRL+C aby przerwać${NC}"
read -n 1 -s

echo -e "${YELLOW}No to lecimy!${NC}"

# tworzymy Dockerfile
cat <<EOF >Dockerfile
FROM node:22.11.0-bullseye-slim

RUN apt update &&     apt install -y --no-install-recommends ca-certificates libcairo2-dev libpango1.0-dev jq curl unzip make build-essential git nano vim mc &&     curl -fsSL https://bun.sh/install | bash && mv /root/.bun/bin/bun /bin/bun && echo "\nPS1='\[\033[32m\]AIDEVS\[\033[0m\]:\w\$ '\n" >>/root/.bashrc &&   mkdir /app/ && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PKG_CONFIG_PATH=/usr/lib/pkgconfig

WORKDIR /app

EXPOSE $PORT

CMD ["/bin/bash"]
EOF

# lecimy z kodem
if [ -d "3rd-devs" ]; then
    echo -e "${YELLOW}Odświeżam repo${NC}"
    cd 3rd-devs
    git checkout .
    cd ..
else
    echo -e "${GREEN}Klonuję repo${NC}"
    git clone https://github.com/i-am-alice/3rd-devs
fi

# czas na obraz kontenera

oldContainer=$(docker ps -a -q -f name=ai_container)
if [ -z "$oldContainer" ]; then
    echo -e "${GREEN}Brak aktywnego kontenera${NC}"
else
    docker stop $oldContainer
    docker rm $oldContainer
    echo -e "${YELLOW}Stary kontener $oldContainer został zatrzymany i usunięty${NC}"
fi

if docker image inspect aidevs3 >/dev/null 2>&1; then
    docker rmi aidevs3
    echo -e "${YELLOW}Stary obraz aidevs3 został usunięty${NC}"
fi

echo -e "${GREEN}Budowanie obrazu aidevs3 z Dockerfile${NC}"
export DOCKER_BUILDKIT=1
echo ${PWD}
docker build --no-cache -t aidevs3 .

if [ $? -ne 0 ]; then
    echo -e "${RED}Błąd podczas budowania obrazu X_X${NC}"
    exit 2
fi

# instalacja paczek
docker run --rm -it --name aidevs_tmp -v ${PWD}/3rd-devs:/app aidevs3 /bin/bash -c "cd /app && bun install --trust-all && bun install promptfoo@0.82.0 --trust-all && ln -s /app/node_modules/.bin/pf /usr/bin/pf && ln -s /app/node_modules/.bin/promptfoo /usr/bin/promptfoo && bun pm trust --all"

# uruchamiamy kontener
echo -e "${GREEN}Aby rozpocząć pracę ze środowiskiem, uruchom poniższe polecenie:${NC}\n\n"

echo -e "${YELLOW}docker run --rm -it -p $PORT:3000 --name aidevs -v \${PWD}/3rd-devs:/app aidevs3${NC}"
