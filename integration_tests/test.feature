Feature: Basic functionality
  Scenario: Obtain event and then check whether it was logged
     Given Container is running
      # Bevare this could take some time its
      # making requests to the internet.
      Then Check container logs for "60" received elements from "npm"
      And Check container logs for "40" received elements from "pypi"
