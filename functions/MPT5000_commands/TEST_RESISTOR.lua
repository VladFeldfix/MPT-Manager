-- Test Resistor
Resistor(
  {
    label='Test RESNAME OHM Ohm',
    device='msr',
    setup = {i = 0.1, Kelvin = 0, tare = {mode = 'fixed', data = {res = 2.5}}},
    criteria = {r = OHM Ohm +- 1%},
    terminals = {test = POINT1, com = POINT2}
  }
)