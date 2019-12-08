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
sudo docker run lazy-nicehash2 &
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
sudo docker run lazy-nicehash2 &
```

---

> If my code was useful for you may buy me tea: 

> BTC 1LTwU8hVYxxpHUDf3wYNDjnS9kK4PDdtgT

> ETH 0x23913F4ab3839a8b7bB987F348b8d974C045Dd17
