Feature: A World to contain objects and lights

As a modeller
I want to have a world
So I can put my objects and lights somewhere


Scenario: Creating a world
Given w <- world()
Then w contains no objects
And w has no light source
