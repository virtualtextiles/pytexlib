from fiberlib import *
from yarnlib import *
from textilelib import *

import math

# one fiber in yarn (monofilament) in x Direction
fi=fiber()
fi.diameter=2.2
fi.setcolour(123,23,230)
fi.append_point(1,2,3)
fi.append_point(3,2,3)
fi.append_point(4,3,3)
fi.append_point(10,2,3)

# Create Yarn ya
ya=yarn()
ya.add_fiber(fi)

# Two fibers along Z Direction
fi2=fiber()
fi2.setcolour(123,230,230)
fi2.diameter=3
for i in range (0,10):
    fi2.append_point(1.4*math.sin(i),1.4*math.cos(i),i)

fi3=fiber()
fi3.setcolour(123,130,230)
fi3.diameter=2
for i in range (0,10):
    fi3.append_point(0.2 + 2.8*math.sin(i+3),3*math.cos(i*0.9+3),i)

#Create yarn ya1
ya1=yarn()
ya1.add_fiber(fi2)
ya1.add_fiber(fi3)

t=textile()
t.add_yarn(ya)
t.add_yarn(ya1)
t.write_file("mysample.csv")

t.plot()