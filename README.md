# complexP
Generate and work with a complex probability system that has components with an exponentially decaying lifetime.
The only dependency is numpy.

Two classes are provided

Component:
- Initialized with:
    l:float, which stands for lambda and defines the rate of exponential decay.
- Contains function:
    self.p(t:float), which provides the probability of itself working at time t.

System:
- Initialized with:
    componentsOrSubsystems:list , is a list of components or other systems which it connects.
    parallel:bool, which states whether the connection is parallel
    series:bool, which states whether the conneciton is in series
- Contains functions:
    self.p(t:float), which provides the total probability of itself working at time t, dynamically
    considering all components and subsystems contained within it.
    self.condprob(t:float), which provides the probability of itself working at time t, conditioned
    on the evidence of a dependent component or dependent subsystem working. 
