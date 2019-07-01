Feature: A World to contain objects and lights

As a modeller
I want to have a world
So I can put my objects and lights somewhere


Scenario: Creating a world
Given w <- world()
Then w contains no objects
And w has no light source

Scenario: The default world
Given light <- point_light(point(-10, 10, -10), colour(1, 1, 1))
And s1 <- sphere() with:
| material.colour | (0.8, 1.0, 0.6) |
| material.diffuse | 0.7 |
| material.specular | 0.2 |
And s2 <- sphere() with:
| transform | scaling(0.5, 0.5, 0.5) |
When w <- default_world()
Then w.lights = light
And w contains s1
And w contains s2
