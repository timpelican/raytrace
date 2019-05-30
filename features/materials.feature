Feature: Materials

As a programmer
I want to make my objects from materials
So I have objects that appear different from each other

Background:
  Given m <- material()
  And position <- point(0, 0, 0)

Scenario: The default material
  Given m <- material()
  Then m.colour = colour(1, 1, 1)
  And m.ambient = 0.1
  And m.diffuse = 0.9
  And m.specular = 0.9
  And m.shininess = 200.0

Scenario: Lighting with the eye between the light and the surface
  Given eyev <- vector(0, 0, -1)
  And normalv <- vector(0, 0, -1)
  And p <- point(0, 0, -10)
  And c <- colour(1, 1, 1)
  And light <- point_light(p, c)
  When result <- lighting(m, light, position, eyev, normalv)
  Then colour result = colour(1.9, 1.9, 1.9)

Scenario: Lighting with the eye between light and surface, eye offset 45 degrees
  Given eyev <- vector(0, 0.7071067811865476, -0.7071067811865476) # sqrt(2)/2
  And normalv <- vector(0, 0, -1)
  And p <- point(0, 0, -10)
  And c <- colour(1, 1, 1)
  And light <- point_light(p, c)
  When result <- lighting(m, light, position, eyev, normalv)
  Then colour result = colour(1.0, 1.0, 1.0)

Scenario: Lighting with eye opposite surface, light offset 45 degrees
  Given eyev <- vector(0, 0, -1)
  And normalv <- vector(0, 0, -1)
  And p <- point(0, 10, -10)
  And c <- colour(1, 1, 1)
  And light <- point_light(p, c)
  When result <- lighting(m, light, position, eyev, normalv)
  Then colour result = colour(0.7364, 0.7364, 0.7364)

Scenario: Lighting with eye in the path of the reflection vector
  Given eyev <- vector(0, -0.7071067811865476, -0.7071067811865476)
  And normalv <- vector(0, 0, -1)
  And p <- point(0, 10, -10)
  And c <- colour(1, 1, 1)
  And light <- point_light(p, c)
  When result <- lighting(m, light, position, eyev, normalv)
  Then colour result = colour(1.6364, 1.6364, 1.6364)

Scenario: Lighting with the light behind the surface
  Given eyev <- vector(0, 0, -1)
  And normalv <- vector(0, 0, -1)
  And p <- point(0, 0, 10)
  And c <- colour(1, 1, 1)
  And light <- point_light(p, c)
  When result <- lighting(m, light, position, eyev, normalv)
  Then colour result = colour(0.1, 0.1, 0.1)
