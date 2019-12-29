Feature: Noise

As a programmer
I want to have a source of noise available
So I can make more organic-looking materials

Scenario: Generating noise
  Given n <- noise()
  Then n.noise_at(0, 0) = 0.0
  And n.noise_at(100, 100) = -0.21884733123299538
