## environment
```bash
conda create -n fastapi python=3.10.9
conda activate fastapi
pip install -r requirements.txt
```

## prepare database
```bash
sqlite3 test.db
>>> .help
```

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title varchar(30),
    release_year varchar(4),
    country varchar(20),
    director_id integer,
    genres text
);

CREATE TABLE actors (
    person_id integer,
    movie_id integer,
    main_role boolean
);

CREATE TABLE persons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name varchar(30),
    birth_date varchar(10),
    type varchar(30)
);

insert into persons (full_name, birth_date, type) values("Will Smith", "25 Sep 1968", "actor");
insert into persons (full_name, birth_date, type) values("Francis Lawrence", "26 Mar 1976", "director");
insert into persons (full_name, birth_date, type) values("Barry Sonnenfeld", "1 Apr 1951", "director");
insert into persons (full_name, birth_date, type) values("Salma Hayek", "2 Sep 1966", "actor");

insert into movies (title, release_year, country, genres, director_id) values("I Am Legend", "2007", "USA", "post-apocalyptic thriller", 2);
insert into actors (person_id, movie_id, main_role) values(1, 1, true);

insert into movies (title, release_year, country, genres, director_id) values("Wild Wild West", "1999", "USA", "western steampunk", 3);
insert into actors (person_id, movie_id, main_role) values(1, 2, true);
insert into actors (person_id, movie_id, main_role) values(4, 2, true);
```

test some queries:
```sql
select * from movies m join persons p on m.director_id=p.id;
select * from persons p join actors a join movies as m on p.id=a.person_id and m.id=a.movie_id;
```

## graphiql web interface
```bash
uvicorn app:app --reload
```
open graphiql web interface in a browser http://127.0.0.1:8000/graphiql
and check queries below;

## queries
get all movies with director info:
```
query {
  movies {
    id
    title
    releaseYear
    country
    director {
      fullName
      birthDate
      type
    }
    genres
  }
}
```

get all movies with actors info:
```
query {
  movies {
    id
    title
    actors {
      fullName
      birthDate
    }
  }
}
```

get all movies produced in USA and released in 2007 (filtering):
```
query {
  movies (filter: {
    country: "USA"
    releaseYear: "2007"
  }) {
    id
    title
    country
    releaseYear
  }
}
```

## mutations
add new movie:
```
mutation {
  addMovie(
    title: "night in Paris"
    releaseYear: "1991"
    directorId: 1
    genres: "thriller"
    country: "Brasil"
  ){
    id
  }
}
```

## note
commit `d85df33` contains start implementation based on `databases` and `sqlalchemy core`