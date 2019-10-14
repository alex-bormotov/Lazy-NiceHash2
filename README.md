# Lazy-NiceHash2

## Features

> Show wallet balances

> Trade on Nicehash Exchange

> Autoexchange mined BTC to other coin, once a day (for instance)

> Show coin prices

---

### Install

```bash
sudo apt-get update
```

```bash
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

```bash
sudo apt-get update
```

```bash
sudo apt-get install docker.io git
```

```bash
git clone https://github.com/alex-bormotov/Lazy-NiceHash2
```

```bash
cd Lazy-NiceHash2
```

```bash
cp config.json.sample config.json
```

> edit config.json

```bash
sudo docker build -t lazy-nicehash2 .
```

```bash
sudo docker run Lazy-NiceHash2 &
```
---

### Update

```bash
cd Lazy-NiceHash2
```

```bash
sudo docker ps
```

```bash
sudo docker stop CONTAINER ID
```

```bash
sudo docker rm CONTAINER ID
```

```bash
sudo docker rmi Lazy-NiceHash2
```

```bash
git pull origin master
```

```bash
sudo docker build -t lazy-nicehash2 .
```

```bash
sudo docker run Lazy-NiceHash2 &
```
---

### Donate

> If you would like to buy me a coffee  3K9ocinkiUUqkBj9BqvFVsUgW2uMLqZFcP (BTC)
