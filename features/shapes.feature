Feature: Shapes

As a programmer
I want to abstract shared properties into shapes
So I can avoid duplicating code

Scenario: The default transformation
  Given s <- test_shape()
  Then s.transform is the identity_matrix

Scenario: Assigning a transformation
  Given s <- test_shape()
  And t <- translation(2, 3, 4)
  When set_transform(s, t)
  Then s.transform = t

Scenario: The default material
  Given s <- test_shape()
  When m <- s.material
  Then material m is the default material

Scenario: Assigning a material
  Given s <- test_shape()
  And m <- material()
  And m.ambient <- 1
  When s.material <- m
  Then s.material = m

Scenario: Intersecting a scaled shape with a ray
  Given r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And s <- test_shape()
  And t <- scaling(2, 2, 2)
  When set_transform(s, t)
  And xs <- intersect(s, r)
  Then s.saved_ray.origin = point(0, 0, -2.5)
  And s.saved_ray.direction = vector(0, 0, 0.5)

Scenario: Intersecting a translated shape with a ray
  Given r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And s <- test_shape()
  And t <- translation(5, 0, 0)
  When set_transform(s, t)
  And xs <- intersect(s, r)
  Then s.saved_ray.origin = point(-5, 0, -5)
  And s.saved_ray.direction = vector(0, 0, 1)

Scenario: Computing the normal on a translated shape
  Given s <- test_shape()
  And t <- translation(0, 1, 0)
  When set_transform(s, t)
  And n <- normal_at(s, point(0, 1.70711, -0.70711))
  Then vector n = vector(0, 0.70711, -0.70711)

Scenario: Computing the normal on a transformed shape
  Given s <- test_shape()
  And m1 <- scaling(1, 0.5, 1)
  And m2 <- rotation_z(0.6283185307179586)
  And m <- m1 * m2
  When set_transform(s, m)
  And n <- normal_at(s, point(0, 0.70711, -0.70711))
  Then vector n = vector(0, 0.97014, -0.24254)
