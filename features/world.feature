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

Scenario: Intersect a world with a ray
  Given w <- default_world()
  And r <- ray(point(0, 0, -5), vector(0, 0, 1))
  When xs <- intersect_world(w, r)
  Then xs.count = 4
  And xs[0].t = 4
  And xs[1].t = 4.5
  And xs[2].t = 5.5
  And xs[3].t = 6

Scenario: Shading an intersection
  Given w <- default_world()
  And r <- ray(point(0, 0, -5), vector(0, 0, 1))
  And shape <- the first object in w
  And i <- intersection(4, shape)
  When comps <- prepare_computations(i, r)
  And c <- shade_hit(w, comps)
  Then colour c = colour(0.38066, 0.47583, 0.2855)

Scenario: Shading an intersection from the inside
  Given w <- default_world()
  And l <- point_light(point(0, 0.25, 0), colour(1, 1, 1))
  And w.light <- l
  And r <- ray(point(0, 0, 0), vector(0, 0, 1))
  And shape <- the second object in w
  And i <- intersection(0.5, shape)
  When comps <- prepare_computations(i, r)
  And c <- shade_hit(w, comps)
  Then colour c = colour(0.90498, 0.90498, 0.90498)

Scenario: The colour when a ray misses
  Given w <- default_world()
  And r <- ray(point(0, 0, -5), vector(0, 1, 0))
  When c <- colour_at(w, r)
  Then colour c = colour(0, 0, 0)

Scenario: The colour when a ray hits
  Given w <- default_world()
  And r <- ray(point(0, 0, -5), vector(0, 0, 1))
  When c <- colour_at(w, r)
  Then colour c = colour(0.38066, 0.47583, 0.2855)

Scenario: The colour with an intersection behind the ray
  Given w <- default_world()
  And outer <- the first object in w
  And outer.material.ambient <- 1
  And inner <- the second object in w
  And inner.material.ambient <- 1
  And r <- ray(point(0, 0, 0.75), vector(0, 0, -1))
  When c <- colour_at(w, r)
  Then colour c = inner.material.colour

Scenario: There is no shadow when nothing is collinear with point and light
  Given w <- default_world()
  And p <- point(0, 10, 0)
  Then is_shadowed(w, p) is false

Scenario: The shadow when an object is between the point and the light
  Given w <- default_world()
  And p <- point(10, -10, 10)
  Then is_shadowed(w, p) is true

Scenario: There is no shadow when an object is behind the light
  Given w <- default_world()
  And p <- point(-20, 20, -20)
  Then is_shadowed(w, p) is false

Scenario: There is no shadow when an object is behind the point
  Given w <- default_world()
  And p <- point(-2, 2, -2)
  Then is_shadowed(w, p) is false

Scenario: shade_hit() is given an intersection in shadow
  Given w <- world()
  And l <- point_light(point(0, 0, -10), colour(1, 1, 1))
  And w.light <- l
  And s1 <- sphere()
  And object s1 is added to world w
  And s2 <- sphere()
  And t <- translation(0, 0, 10)
  And set_transform(s2, t)
  And object s2 is added to world w
  And r <- ray(point(0, 0, 5), vector(0, 0, 1))
  And i <- intersection(4, s2)
  When comps <- prepare_computations(i, r)
  And c <- shade_hit(w, comps)
  Then colour c = colour(0.1, 0.1, 0.1)
