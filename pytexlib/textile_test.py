from fiberlib import *
from yarnlib import *
from textilelib import *

import math

fi=fiber()
fi.setcolour(123,23,230)
fi.append_point(1,2,3)
fi.append_point(12,2,3)
fi.append_point(22,2,3)

fi2=fiber()
fi2.setcolour(123,230,230)
fi2.diameter=2
for i in range (0,10):
    fi2.append_point(10*math.sin(i),3*math.cos(i),i)

fi3=fiber()
fi3.setcolour(123,130,230)
fi3.diameter=2
for i in range (0,10):
    fi3.append_point(1*math.sin(i),3*math.cos(i),i)


ya=yarn()
ya.add_fiber(fi)

ya1=yarn()
ya1.add_fiber(fi2)
   
ya1.add_fiber(fi3)

t=textile()
#t.add_yarn(ya)
t.add_yarn(ya1)
t.write_file("mysample.csv")

t.plot()