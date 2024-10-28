-- Test Capacitor
Capacitor(
  {
    label = 'Test Capacitor CAPNAME',
    device = 'msr',
    setup = {i = 1000 mA, v = 5 V, tare = {mode = 'system'}},
    criteria = {c > MINuF, c < MAXuF},
    terminals = {test = POINT1, com = POINT2}
  }
)