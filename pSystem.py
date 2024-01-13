import numpy as np

class Component:
    """
    Component of a probabilistic system with an exponentially 
    distributed lifetime, where self.l is the lambda parameter 
    in the exponent.

    Class functions:
        p(self, t:float) ->float
            Accepts time as t 
            Returns probability of component working at time t,
            as P(component) = e^(-lambda * t)
    """
    def __init__(self,l:float):
        """
        P(component) = e^(-lambda * t),
        where lambda = self.l
        """
        self.l = l
    
    def p(self,t:float)->float:
        """
        Returns probability of component working at time t,
        where P(component) = e^(-lambda * t),
        and lambda is referenced from object
        """
        # Calls numpy's exponential function
        # returns e^(-lambda * t)
        return np.exp(-self.l * t)


class System:
    """
    Framework for probabilistic systems composed of probabilistic components.
    The System has a probability of working at time t, given by a parallel or series
    connection between the components that compose the system.

    The System's probability of working is calculated by recursing through the system
    and referencing the functions within its Components (which also works with subsystems).

    Once it has calculated the probabilities of all of its components working, then it
    combines them in parallel or in series.

    Class functions:
        p(self,t:float)->float
            Accepts time as t,
            Calculates the probability of system working by recursing through 
            all of its components and then combining them in parallel or in series,
            Returns the probability of system working.
    """
    def __init__(self,
                 componentsAndSubSystems:list=list(), 
                 parallel:bool=False,
                 series:bool=False):
        """
        A system can be composed of individual components or subsystems,
        which are then combined in parallel XOR in series.

        To initialize, provide a list of components and subsystems, 
        as well as a boolean indicator for the type of connection between components. 
        """
        self.comps = componentsAndSubSystems
        self.parallel = parallel
        self.series = series
        
    def p(self,t:float)->float:
        """
        Returns the probability of a system working at time t, recursively taking 
        into account all subsystems and and components. 
        """
        if self.parallel:
            """
            The probability of components working in parallel is given by
            P(E1 ∪ E2) = 1 - qE1 * qE2,
             where qE1 = 1 - pE1, 
                   qE2 = 1 - pE2
            """
            # For a given time, t & component (or subsystem), c
            # generate the component's (or subsystem's) probability
            # of not working at time t.
            # qE = 1 - pE
            generateQ = lambda t, c: 1 - c.p(t)

            # Creates an iterable with the generator inside.
            # Equivalent to:
            # for c in self.comps:
            #   generateQ(t,c)
            Qs = (generateQ(t,c) for c in self.comps)

            # Creates a numpy array from the results of the iterable
            allQ = np.fromiter(Qs,float)

            # Takes the product of all of the results of the iterable
            # returns 1-product of the results.
            return 1-np.prod(allQ)
            
        elif self.series:
            """
            The probability of components working in series is given by
            P(E1 ∩ E2) = pE1 * pE2
            """
            # For a given time, t & component (or subsystem), c
            # generate the component's (or subsystem's) probability
            # of working at time t.  
            generateP = lambda t, c: c.p(t)

            # Creates an iterable with the generator inside.
            # Equivalent to:
            # for c in self.comps:
            #   generateP(t,c)
            Ps = (generateP(t,c) for c in self.comps)

            # Creates a numpy array from the results of the iterable
            allP = np.fromiter(Ps,float)
            
            # Returns the product of all of the results of the iterable
            return np.prod(allP)

    def condProb(self, dependence, t, negate:bool=False)->float:
        """
        Returns the probability of a system working at time t, 
        conditioned on a component or subsystem that it is 
        dependent upon.

        The conditioning can be negated as well, resulting in 
        the probability of the system working in the case that
        the dependence does not work at time t.
        """
        if negate:
            # Return the probability that it works, if the 
            # component or subsystem it is dependent upon 
            # does not work. 
            # Equivalent to: P(S|-Dependence)
            return self.p(t)*(1-dependence.p(t))

        # Return the probability that it works, if the 
        # component or subsystem it is dependent upon 
        # works.
        # Equivalent to: P(S|Dependence)
        return self.p(t)*dependence.p(t)