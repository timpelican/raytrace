Feature: Materials

As a programmer
I want to make my objects from materials
So I have objects that appear different from each other

Scenario: The default material
  Given m <- material()
  Then m.colour = colour(1, 1, 1)
  And m.ambient = 0.1
  And m.diffuse = 0.9
  And m.specular = 0.9
  And m.shininess = 200.0
