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
    [] clean and normalize by population
    [] add the monthly overdose data source you found
    [] scrap the exploratory functionality in the pull data classes, keep it simple
    [] set up sqlalchemy model
    [] set up migrations
    [] analyze
    [] hypothesize
    [] export to bokeh viz
    [] embed on pages
    [] write blurb?  self-updating?

# Backend/ETL Version 1
![back end 1](/assets/etl-1.png)
## Hypothetical Population Normalization Module
![pop normal](/assets/pop-norm.png)

# Front End Version 1
![front end 1](/assets/front-end-1.jpg)

# Database Structure Version 1
![db structure 1](/assets/db-1.png)
