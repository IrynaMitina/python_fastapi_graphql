```bash
pip install fastapi
pip install uvicorn
pip install 'strawberry-graphql[fastapi]'
pip install aiosqlite
pip install databases
pip install sqlalchemy
```

```bash
sqlite3 test.db
>>> .help
```

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title varchar(30),
    description text,
    premiere_date varchar(10)
);
insert into movies (title, description, premiere_date) values("The Dark", "german, suspense, series", "2018-01-02");
insert into movies (title, description, premiere_date) values("Catch me if you can", "usa, thriller", "2015-11-24");
```

```bash
uvicorn app:app --reload
```
open graphiql web interface in a browser http://127.0.0.1:8000/graphiql
and check queries below;

get all movies:
```
query {
  movies {
    id
    title
    description
    premiereDate
  }
}
```

add new movie:
```
mutation {
  addMovie(
    title: "Trust"
    description: "money"
    premiereDate: "2020-11-27"
  ) {
    id
    title
  }
}
```