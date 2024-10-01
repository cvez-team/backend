# CVEZ Backend

> Back-end for CVEZ - An tool for speed up recruitment process with Auto matching CV and Virtual Interview.

## 🚀 How to run

### Prerequisites

- Provide `.env` file at the root folder before run this project. _Contact `cvezteam@gmail.com` for become mantainer_.

- Python 3.10 or [Docker Engine](https://docs.docker.com/engine/)

### Clone this Repository

```sh
git clone https://github.com/cvez-team/backend cvez-backend
```

### Run Locally

1. With Docker **(Recommended)**

```sh
docker compose up
```

2. With Python

- Run Redis locally. [Detail](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/docker/)

```sh
docker run --rm -d --name redis -p 6379:6379 -v $pwd/data/redis_storage/:/data redis/redis-stack-server:latest
```

- Run Qdrant VectorDB locally. [Detail](https://qdrant.tech/documentation/quickstart/)

```sh
docker run --rm -d --name qdrant -p 6333:6333 -p 6334:6334 -v $pwd/data/qdrant_storage:/qdrant/storage:z qdrant/qdrant
```

- Run MongoDB locally. [Detail](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-community-with-docker/)

```sh
# Create Docker volume
docker volume create mongodbdata
# Start Mongodb container
docker run --rm -d --name mongodb -p 27017:27017 -v mongodbdata:/data/db mongodb/mongodb-community-server:latest
```

- Create Virtual environment (Optional)

```sh
# Create virtual environment
python -m venv env

# Set virtual environment as interpreter
env/Scripts/activate # Windows
source env/bin/activate # Linux | MacOS
```

- Install dependencies

```sh
pip install -r requirements.txt
```

- Start server. Server will served at `localhost:7860`

```sh
python main.py
```

## 📖 Maintain documents

### Development Document

1. [Overview](/docs/Development/1.%20Overview.md)
   - Technologies
   - Pipeline
   - Code Structure
   - Algorithm
2. Versioning & Module
   - Git Convension
   - Version
   - Module Roles
3. [Database](/docs/Development/3.%20Database.md)
   - Cache Database
   - Document Database
   - Vector Database
4. Algorithm
   - Testing System
   - Testing Dataset
   - Metrics

### Deployment Document

1. Overview
   - Cloud Platform
2. CI/CD
3. Terraform
