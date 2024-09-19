## TRELLO EXAMPLE PROJECT 
[![python](https://img.shields.io/badge/python-3.12-ffdb66?style=flat&labelColor=255073)](https://www.python.org/)
[![python](https://img.shields.io/badge/sqlalchemy-a30000)](https://www.sqlalchemy.org)
[![python](https://img.shields.io/badge/docker-255073)](https://www.docker.com)
[![python](https://img.shields.io/badge/docker--compose-orange)](https://github.com/docker/compose)
[![python](https://img.shields.io/badge/postgres-blue)](https://www.postgresql.org)


## Installation 

 - Install Docker

```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

- Install docker-compose

```bash
  sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  sudo chmod +x /usr/local/bin/docker-compose
  ```

- Clone repository From Git

```bash
  git clone https://github.com/andmayster/trello-example.git
```

- Firstly you need create .env file or copy it on directory trello-example
```bash
  cd trello-example
  ```

- Enter command for create file
```bash
  sudo nano .env
  ```

- The file should look like this

    <details>
    <summary><i><b>.env</b> </i></summary>
  
      POSTGRES_PASSWORD=trello-example-password
      POSTGRES_USERNAME=trello
      POSTGRES_PORT=5432
      POSTGRES_DBNAME=database-trello
      POSTGRES_HOST=postgresql
      SECRET_KEY=f70b373625cff18005d687be35b87e838645171f3ab1638bfb22fc5ca0198ce7
      REFRESH_SECRET_KEY=16f307298b11d78529e3936352e7c221548d241b76ee5cb35f1f4c5b998de57e
      SESSION_SECRET_KEY=ff61069b6a5cf447a5f284b2da93f84de3524c4c8073db165a987ba615ec6383

    </details>

- **When .env file created, you can start APP** 
###### (at this stage, docker containers will be creating and launch)
```bash
  docker-compose up -d
  ```

- **To stop APP - enter the following command**
```bash
  $ docker-compose down
  ```

### After starting the application, you can access the API at the following address:
```bash
  http://localhost:8000 
  ```

### swagger documentation
```bash
  http://localhost:8000/swagger
  ```

