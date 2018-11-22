Feature: Basic functionality
  Scenario: Obtain packages for npm and then check whether it was logged
     Given Container is running
      # Bevare this could take some time its
      # making requests to the internet.
      Then Check container logs for "60" received elements from "npm"

  Scenario: Obtain packages for pypi and then check whether it was logged
     Given Container is running
      Then Check container logs for "40" received elements from "pypi"
