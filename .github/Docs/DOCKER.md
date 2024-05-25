<h1 align="center">Docker</h1>

install docker+docker compose (or docker desktop)

## **running**
make .env file 

**if commands fail, "docker compose" instead of "docker-compose"**

To run the bot, simply execute the following command in the root of the project:
```bash
docker-compose up -d
```
↑ builds container and runs in detached mode.
↓ shows logs
```bash
docker-compose logs -f
```

↓ stops container
```bash
docker-compose down
```
## **update:**
stop container, clone, restart with ↓
```bash
docker-compose build
docker-compose up -d
```