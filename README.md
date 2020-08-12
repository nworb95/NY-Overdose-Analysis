# "Overdose" Analysis Framework

Potential future framework for econometric journalism.

Inputs include public data source APIs to hit, and outputs will be a Kibana dashboard -- ideally hosted on my future website, but for the near term just standalone.  Microservices will be written in languages I am interested in dabbling in eg maybe a basic multiprocessor written in Go.  

I switched from VS Code back to PyCharm midway so some of the doc strings aren't even matching yet.

# Requirements

Have an environment variable called `SOCRATA_TOKEN` with your Socrata Token.

# How to Use

```
docker-compose build
docker-compose up
```

# TODOs
    * Pull data IF NOT exists
    * Clean & normalize by population, impute missing numbers
    * upload to elasticsearch
    * (explore)
    * regress
    * export dashboard to host server -- heroku?
