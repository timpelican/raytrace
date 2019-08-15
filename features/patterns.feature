Feature: Patterns

As a modeller
I want to apply patterns to my objects
So they look more interesting

Background:
  Given black <- colour(0, 0, 0)
  And white <- colour(1, 1, 1)

Scenario: Creating a stripe pattern
  Given pattern <- stripe_pattern(white, black)
  Then pattern.a = colour white
  And pattern.b = colour black

Scenario: A stripe pattern is constant in y
  Given pattern <- stripe_pattern(white, black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0, 1, 0)) = colour white
  And stripe_at(pattern, point(0, 2, 0)) = colour white

Scenario: A stripe pattern is constant in z
  Given pattern <- stripe_pattern(white, black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0, 0, 1)) = colour white
  And stripe_at(pattern, point(0, 0, 2)) = colour white

Scenario: A stripe pattern alternates in x
  Given pattern <- stripe_pattern(white, black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0.9, 0, 0)) = colour white
  And stripe_at(pattern, point(1, 0, 0)) = colour black
  And stripe_at(pattern, point(-0.1, 0, 0)) = colour black
  And stripe_at(pattern, point(-1, 0, 0)) = colour black
  And stripe_at(pattern, point(-1.1, 0, 0)) = colour white
