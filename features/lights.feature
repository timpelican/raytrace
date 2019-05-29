Feature: Lights

As a programmer
I want to have lights in my scene
So I have objects that aren't in the dark

Scenario: A point light has a position and intensity
  Given intensity <- colour(1, 1, 1)
  And position <- point(0, 0, 0)
  When light <- point_light(position, intensity)
  Then light.position = position
  And light.intensity = intensity
