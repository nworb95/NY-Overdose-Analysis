# "Overdose" Analysis Framework

Potential future framework for econometric journalism.

Inputs include public data source APIs to hit, and the output will be a simple interactive map of NY county-level data.  I will use Bokeh for the visualization, sqlalchemy + Postgres for the database, and Flask for the webserver.

# Requirements

Have an environment variable called `SOCRATA_TOKEN` with your Socrata Token.

# How to Use

```
make docker-run
```

# TODOs
    * clean and normalize by population
    * set up sqlalchemy model
    * analyze
    * hypothesize
    * export to bokeh viz

# Database Structure Version 1

![db structure 1](/assets/db-1.png)