Feature: Patterns

As a modeller
I want to apply patterns to my objects
So they look more interesting

Background:
  Given black <- colour(0, 0, 0)
  And white <- colour(1, 1, 1)
  And s_black <- solid_colour(black)
  And s_white <- solid_colour(white)

Scenario: Creating a stripe pattern
  Given pattern <- stripe_pattern(s_white, s_black)
  Then pattern.a = solid_colour s_white
  And pattern.b = solid_colour s_black

Scenario: A stripe pattern is constant in y
  Given pattern <- stripe_pattern(s_white, s_black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0, 1, 0)) = colour white
  And stripe_at(pattern, point(0, 2, 0)) = colour white

Scenario: A stripe pattern is constant in z
  Given pattern <- stripe_pattern(s_white, s_black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0, 0, 1)) = colour white
  And stripe_at(pattern, point(0, 0, 2)) = colour white

Scenario: A stripe pattern alternates in x
  Given pattern <- stripe_pattern(s_white, s_black)
  Then stripe_at(pattern, point(0, 0, 0)) = colour white
  And stripe_at(pattern, point(0.9, 0, 0)) = colour white
  And stripe_at(pattern, point(1, 0, 0)) = colour black
  And stripe_at(pattern, point(-0.1, 0, 0)) = colour black
  And stripe_at(pattern, point(-1, 0, 0)) = colour black
  And stripe_at(pattern, point(-1.1, 0, 0)) = colour white

Scenario: Stripes with an object transformation
  Given object <- sphere()
  And set_transform(object, scaling(2, 2, 2))
  And pattern <- stripe_pattern(s_white, s_black)
  When c <- stripe_at_object(pattern, object, point(1.5, 0, 0))
  Then colour c = colour white

Scenario: Stripes with a pattern transformation
  Given object <- sphere()
  And pattern <- stripe_pattern(s_white, s_black)
  And set_pattern_transform(pattern, scaling(2, 2, 2))
  When c <- stripe_at_object(pattern, object, point(1.5, 0, 0))
  Then colour c = colour white

Scenario: Stripes with both an object and a pattern transformation
  Given object <- sphere()
  And set_transform(object, scaling(2, 2, 2))
  And pattern <- stripe_pattern(s_white, s_black)
  And set_pattern_transform(pattern, translation(0.5, 0, 0))
  When c <- stripe_at_object(pattern, object, point(2.5, 0, 0))
  Then colour c = colour white

Scenario: The default pattern transformation
  Given pattern <- test_pattern()
  Then pattern.transform is the identity_matrix

Scenario: Assigning a transformation
  Given pattern <- test_pattern()
  When set_pattern_transform(pattern, translation(1, 2, 3))
  And t <- translation(1, 2, 3)
  Then pattern.transform = t

Scenario: A pattern with an object transformation
  Given shape <- sphere()
  And set_transform(shape, scaling(2, 2, 2))
  And pattern <- test_pattern()
  When c <- pattern_at_shape(pattern, shape, point(2, 3, 4))
  Then colour c = colour(1, 1.5, 2)

Scenario: A pattern with a pattern transformation
  Given shape <- sphere()
  And pattern <- test_pattern()
  And set_pattern_transform(pattern, scaling(2, 2, 2))
  When c <- pattern_at_shape(pattern, shape, point(2, 3, 4))
  Then colour c = colour(1, 1.5, 2)

Scenario: A pattern with both an object and a pattern transformation
  Given shape <- sphere()
  And set_transform(shape, scaling(2, 2, 2))
  And pattern <- test_pattern()
  And set_pattern_transform(pattern, translation(0.5, 1, 1.5))
  When c <- pattern_at_shape(pattern, shape, point(2.5, 3, 3.5))
  Then colour c = colour(0.75, 0.5, 0.25)

Scenario: A gradient linearly interpolates between colours
  Given pattern <- gradient_pattern(s_white, s_black)
  Then pattern_at(pattern, point(0, 0, 0)) = colour white
  And pattern_at(pattern, point(0.25, 0, 0)) = colour(0.75, 0.75, 0.75)
  And pattern_at(pattern, point(0.5, 0, 0)) = colour(0.5, 0.5, 0.5)
  And pattern_at(pattern, point(0.75, 0, 0)) = colour(0.25, 0.25, 0.25)

Scenario: A bi-gradient linearly interpolates between colours and back again
  Given pattern <- bigradient_pattern(s_white, s_black)
  Then pattern_at(pattern, point(0, 0, 0)) = colour white
  And pattern_at(pattern, point(0.25, 0, 0)) = colour(0.5, 0.5, 0.5)
  And pattern_at(pattern, point(0.5, 0, 0)) = colour black
  And pattern_at(pattern, point(0.75, 0, 0)) = colour(0.5, 0.5, 0.5)
