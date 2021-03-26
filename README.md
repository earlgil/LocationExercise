# GeoDataExercise
Repository created for geodata exercise
### Create API using Python to identify state from address provided by user.
### Utilize google mapping API, Docker, and PostgreSQL
### Get user address input in POST endpoint (/location) formatted as:

###{
###  ...."address": "1234 Main Street Anycity, AA 55555"
###}

### Google API will identify longitude and latitude coordinates
### These coordinate are queried in PostGIS database in container
### The state is returned in query result and provided to user in GET endpoint (/location) 
## 
## 
