from ._dsp import DiscreteStochasticProcess as DSP
from ..variables import RandVar
from ..samples import Sample
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

class RandWalk(DSP):
    """
    
    Summary
    -------
    The random walk is a famous discrete, stochastic process. Here
    the ``RandWalk`` class is, accordingly, a subclass of the 
    ``DiscreteStochasticProcess`` class. The n-th random variable in 
    the random walk process is a sum of n-many independent, discrete 
    (binomial) random variables.

    """
    # custom probabilities
    p: float = 0.5
    q: float = 0.5

    def __init__(self, time_steps: int, **kwargs) -> None:
        """Constructor method
        
        Parameters
        ----------
        time_steps : int
            to be passed to the parent class
        
        p : float, optional
            custom success probability, default is p = 0.5 

        """
        super().__init__(time_steps)
        self.title = f"{RandWalk.__name__}"

        # pass custom success probability p if desired; ensure 0 <= p <= 1
        try:
            self.p = kwargs['p']
            self.q = 1 - self.p
        except KeyError:
            pass 

    def generate_process(self) -> list:
        """Generate the random walk process

        Summary
        -------
        Generate and store in memory (i.e., as a class attribute) 
        the stochastic process as determined by the ``RandWalk``
        class instance

        """
        name = sp.Symbol('0')
        rv = RandVar(**{'name': name, 'pspace': {Sample(name=name, value=0): 1.0}})
        process: list = [rv]
        for i in range(self.time_steps-1):
            name = sp.Symbol(f"X_{i}")
            pspace: dict = {Sample(name=name, value=-1): self.p, Sample(name=name, value=1): self.q}
            rv += RandVar(**{'name': name, 'pspace': pspace})
            process += [rv]

        self.process: list = process

    def plt(self):
        """display generic plot through method inherited from the parent class"""
        self.generate_process()
        self.plot_process()

    def walk_data(self, steps: int) -> np.ndarray:
        """Walk
        
        Parameters
        ----------
        steps : int
            the number of steps to take in total during the random walk process

        Returns
        -------
        out : list[float]
            a cumulative sum of steps taken along the random walk 

        """
        name = sp.Symbol('X')
        rv = RandVar(**{'name': name, 'pspace': {Sample(name=name, value=1): self.p, Sample(name=name, value=-1): self.q}})
        out = rv.generate(iterations=steps)
        out = np.insert(out, 0, 0)
        return out.cumsum()       

    def plt_walk(self, steps: int) -> None:
        """generate and plot the results of ``walk_data``"""
        y = self.walk_data(steps)

        plt.title("Random walk")
        plt.xlabel("Steps")
        plt.ylabel("Net distance")
        plt.plot(y)        
        plt.show()
    
    def plt_walks(self, steps: int, **kwargs) -> None:
        """Simultaneous walks

        Summary
        -------
        Generate plots showing the results of ``time_steps``-many simulations
        of the ``RandWalk`` discrete stochastic process.
        
        Parameters
        ----------
        steps : int
            the number of steps to take for each ``RandWalk`` simulation

        ncols : int, optional
            parameter for formatting the subplots display, default is ncols = 2

        nrows : int, optional
            parameter for formatting the subplots display, default as derived from ncols

        Returns
        -------
        plot : matplotlib.pyplot.subplots
            display subplots of each simulated ``RandWalk`` process

        """
        time_steps: int = self.time_steps
        if time_steps == 1:
            return self.plt_walk()
        
        try:
            ncols: int = kwargs['ncols']
            nrows: int = kwargs['nrows']
        except KeyError:
            ncols = 2
            nrows = sum(divmod(time_steps, ncols))

        try:
            FIGSIZE: tuple = kwargs['FIGSIZE']
        except KeyError:
            FIGSIZE: tuple = (15, 8)

        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=FIGSIZE, squeeze=False)
        fig.suptitle(f"{time_steps} Random Walks")
        for i in range(nrows):
            for j in range(ncols):
                try:
                    index = ncols*i + j
                    y: np.ndarray = self.walk_data(steps)
                    axs[i, j].set_title(f"Walk no. {index+1}")
                    axs[i, j].set_xlabel("steps")
                    axs[i, j].set_ylabel("net distance")
                    axs[i, j].plot(y)

                except IndexError:
                    axs[i, j].axis("off")
        
        plt.tight_layout()
        plt.show()
