# 3D-printer-time-calculator
Calculates total time to 3D print a part

Reads the .gcode of a 3D solid and calculates the total time to print.

The calculation is based on the trapezoidal profile speed for the nozzle.

For that, it is required to know the following:

Vj = jerk speed of the nozzle - mm/s

ac = default nozzle acceleration - mm/s^2

amax = maximum nozzle acceleration - mm/s^2
