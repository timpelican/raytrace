Feature: Intersections

As a programmer
I want to know where rays intersect objects
So I know which objects to render


Scenario: An intersection encapsulates t and object
Given s <- sphere()
When i <- intersection(3.5, s)
Then i.t = 3.5
And i.object = object s

Scenario: Aggregating intersections
  Given s <- sphere()
  And i1 <- intersection(1, s)
  And i2 <- intersection(2, s)
  When xs <- intersections(i1, i2)
  Then xs.count = 2
  And xs[0].t = 1
  And xs[1].t = 2

Scenario: The hit, when all intersections have positive t
  Given s <- sphere()
  And i1 <- intersection(1, s)
  And i2 <- intersection(2, s)
  And xs <- intersections(i2, i1)
  When i <- hit(xs)
  Then hit i = i1

Scenario: The hit, when some intersections have negative t
  Given s <- sphere()
  And i1 <- intersection(-1, s)
  And i2 <- intersection(1, s)
  And xs <- intersections(i2, i1)
  When i <- hit(xs)
  Then hit i = i2

Scenario: The hit, when all intersections have negative t
  Given s <- sphere()
  And i1 <- intersection(-2, s)
  And i2 <- intersection(-1, s)
  And xs <- intersections(i2, i1)
  When i <- hit(xs)
  Then hit i is nothing

Scenario: The hit is always the lowest non-negative intersection
  Given s <- sphere()
  And i1 <- intersection(5, s)
  And i2 <- intersection(7, s)
  And i3 <- intersection(-3, s)
  And i4 <- intersection(2, s)
  And xs <- intersections(i1, i2, i3, i4)
  When i <- hit(xs)
  Then hit i = i4

Scenario: Precomputing the state of an intersection
  Given r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And shape <- sphere()
  And i <- intersection(4, shape)
  When comps <- prepare_computations(i, r)
  Then comps.t = i.t
  And comps.object = i.object
  And comps.point = point(0, 0, -1)
  And comps.eyev = vector(0, 0, -1)
  And comps.normalv = vector(0, 0, -1)

Scenario: The hit, when an intersection occurs on the outside
  Given r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And shape <- sphere()
  And i <- intersection(4, shape)
  When comps <- prepare_computations(i, r)
  Then comps.inside is false

Scenario: The hit, when an intersection occurs on the inside
  Given r <- ray(point(0, 0, 0), vector(0, 0, 1))
  And shape <- sphere()
  And i <- intersection(1, shape)
  When comps <- prepare_computations(i, r)
  Then comps.point = point(0, 0, 1)
  And comps.eyev = vector(0, 0, -1)
  And comps.inside is true
  # normal would have been (0, 0, 1), but is inverted!
  And comps.normalv = vector(0, 0, -1)

Scenario: The hit should offset the point
  Given r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And shape <- sphere()
  And t <- translation(0, 0, 1)
  And set_transform(shape, t)
  And i <- intersection(5, shape)
  When comps <- prepare_computations(i, r)
  Then comps.over_point.z < -0.000005
  And comps.point.z > comps.over_point.z

Scenario: Precomputing the reflection vector
  Given shape <- plane()
  And r <- ray(point(0, 1, -1), vector(0, -0.70710678, 0.70710678))
  And i <- intersection(1.41421356, shape)
  When comps <- prepare_computations(i, r)
  Then comps.reflectv = vector(0, 0.70710678, 0.70710678)
