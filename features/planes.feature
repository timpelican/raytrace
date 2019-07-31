Feature: Planes

As a programmer
I want to work with planes
So I can build objects

Scenario: The normal of a plane is constant everywhere
  Given p <- plane()
  When n1 <- local_normal_at(p, point(0, 0, 0))
  And n2 <- local_normal_at(p, point(10, 0, -10))
  And n3 <- local_normal_at(p, point(-5, 0, 150))
  Then vector n1 = vector(0, 1, 0)
  And vector n2 = vector(0, 1, 0)
  And vector n3 = vector(0, 1, 0)

Scenario: Intersect with a ray parallel to the plane
  Given p <- plane()
  And r <- ray(point(0, 10, 0), vector(0, 0, 1))
  When xs <- local_intersects(p, r)
  Then xs is empty

Scenario: Intersect with a coplanar ray
  Given p <- plane()
  And r <- ray(point(0, 0, 0), vector(0, 0, 1))
  When xs <- local_intersects(p, r)
  Then xs is empty

Scenario: A ray intersecting a plane from above
  Given p <- plane()
  And r <- ray(point(0, 1, 0), vector(0, -1, 0))
  When xs <- local_intersects(p, r)
  Then xs.count = 1
  And xs[0].t = 1
  And xs[0].object = object p

Scenario: A ray intersecting a plane from below
  Given p <- plane()
  And r <- ray(point(0, -1, 0), vector(0, 1, 0))
  When xs <- local_intersects(p, r)
  Then xs.count = 1
  And xs[0].t = 1
  And xs[0].object = object p
