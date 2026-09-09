from pytexlib.structures import Fiber,Yarn,Textile,YarnGroup
import vedo
import math

# one fiber in yarn (monofilament) in x Direction
fi=Fiber()
fi.diameter=.1
fi.set_color(123,23,230)
fi.append_point(1,2,3)
fi.append_point(3,2,3)
fi.append_point(4,3,3)
fi.append_point(10,2,3)

# Create Yarn ya
ya=Yarn()
ya.add_fiber(fi)

# Two fibers along Z Direction
fi2=Fiber()
fi2.set_color(123,230,230)
fi2.diameter=1
for i in range (0,10):
    fi2.append_point(1.4*math.sin(i),1.4*math.cos(i),i)

fi3=Fiber()
fi3.set_color(123,130,230)
fi3.diameter=.5

for i in range (0,10):
    fi3.append_point(0.2 + 2.8*math.sin(i+3),3*math.cos(i*0.9+3),i)

#Create yarn ya1
ya1=Yarn()
ya1.add_fiber(fi2)
ya1.add_fiber(fi3)

#Create yarn Groups
yg_0=YarnGroup()
yg_0.add_yarn(ya)

yg_1=YarnGroup([ya1])

t=Textile(yarn_groups=[yg_0])

t.add_yarn_group(yg_0)
t.add_yarn_group(yg_1)


t.to_reco("./examples/reco_export_example")

vedo.show(t.as_vedo_assembly()).interactive().close()
