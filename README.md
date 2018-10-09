# fabric8-analytics-release-monitor
Service for monitoring of latest updates to upstream packages


### Configuration
Release monitor is configurable by following environment variables.

NPM_URL - http adress of npmjs registry 

PYPI_URL - http adress of pypi registry
 
ENABLE_SCHEDULING - Boolean variable for development and debuging purposes. If true no new jobs will be scheduled.
  
SLEEP_INTERVAL - interval between fetching latest RSS feeds from registries
