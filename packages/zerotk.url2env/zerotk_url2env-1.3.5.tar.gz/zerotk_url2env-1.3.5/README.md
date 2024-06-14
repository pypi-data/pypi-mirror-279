# url2env

Turns database URLs into shell environment variables.

### Usage:

```
$ url2env psql://joebloggs:secret@db.example.com:4433/blog
PGUSER=joebloggs
PGPASSWORD=secret
PGHOST=db.example.com
PGPORT=4433
PGDATABASE=blog
```

With all options:

```
$ url2env --engine --export --prefix=DB_ psql://joebloggs:secret@db.example.com:4433/blog
export DB_ENGINE=psql
export DB_USER=joebloggs
export DB_PASSWORD=secret
export DB_HOST=db.example.com
export DB_PORT=4433
export DB_DATABASE=blog
```


The output could be used in conjunction with `eval`, e.g.::

```
$ eval $(url2env $DATABASE_URL)
```


### Installation

```
$ pip install zerotk.url2env
```


### Distribution

```
$ git tag <x.y>
$ make build upload
```
