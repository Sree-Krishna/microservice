# for installing psycopg
```
export PATH=/Applications/Postgres.app/Contents/Versions/16/bin:$PATH 
```

# for installing psycopg in docker
```
RUN apt-get update \
    && apt-get -y install libpq-dev gcc
RUN python3 -m pip install -r requirements.txt --no-cache-dir
```

docker-compose down    
docker-compose up --build

