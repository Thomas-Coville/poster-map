# poster-map

Poster map is a very simple API that allows creating and downloading High Definition images of google maps with custom styling to print posters.


This project is a pet project that I used to learn python. As a Python beginner, I will appreciate your advices on how to make it better and more pythonic.
The objectives were to learn:
- How to expose a REST Api in Python
- How to run background asynchronous tasks
- Interact with MongoDB
- Configuration Management
- Docker image layering in Python
- Get Familiar with the Python syntax
- Class definitions and inheritance in Python
- Create mental bridges with C# concepts that I am more familiar with


# Usage

For Convenience, [docker compose](docker-compose.yml) at the root will bootstrap the entire stack:
- MongoDB
- Redis
- Celery Worker
- Flask App
- Flower (Celery dashboard)

## Google Static Maps API Key

This project makes calls to the google maps API. you need to provide a valid google API key in order to do the calls: https://developers.google.com/maps/documentation/maps-static/intro

the only place where this API key is used is [in the map generator](generator.py)


There are 2 ways to configure the API key:
## 1. Environment Variable injection [preferred]
modify the [docker compose](docker-compose.yml) file to inject a `DYNACONF_GOOGLE_STATIC_MAPS_API_KEY` env variable in the worker container (the other should not need it at they do not attempt to resolve this config)

```
 worker:
    build:
      context: posters
      dockerfile: Dockerfile  
    depends_on:
      - redis
      - mongo
    command: celery -A entrypoint_celery.celery worker --loglevel=info
    environment:
[...]
    - DYNACONF_GOOGLE_STATIC_MAPS_API_KEY ="YOUR API KEY HERE"    
    volumes:
    - "./output:/output"
```
> the `DYNACONF_` prefix is mandatory for the config management tool to pick it up.
> https://dynaconf.readthedocs.io/en/latest/guides/environment_variables.html

## 2. .secrets.toml
use the `dynaconf` CLI
```
cd posters/
pip install dynaconf
dynaconf write py -s GOOGLE_STATIC_MAPS_API_KEY='you-api-key' 
```
this will create a `.secrets.toml` file that will be copied inside the docker container



# Lesson Learns & Gotchas
- Doing Python development on Windows is HARD:
- virtualenv powershell script does not work in my CMDER shell (readonly prompt)
- Celery 4+ does not support windows officially and probably crashes under the hood. I spend one full day figuring out why my tasks were not being sent to the broker. I still haven't figured precisely why it doesn't worked but it works fine within a docker container.
- the Flask integration with Marshmallow 3+ seems flaky, I had to fix it to the latest 2.x.x version
- kombu 4.6.5+ seems to cause an issue with Flower, stick to the 4.6.3 version

# Next Steps
- UI to front the API
- VSCode configuration
- Logging
- Unit Tests
- Build Script
- Customize Map Styling
- Images and Jobs Eviction
- Cloud deployment and Terraform
- Swagger definition
- Error handling


# Credits
- the Original algorithm to build high res google maps extract can be found here: https://github.com/kuboris/high-def-gmap-export
- This example of Flask & Celery https://github.com/zenyui/celery-flask-factory has been extremely useful to identify that the problem was not 'me' but the Windows integration 