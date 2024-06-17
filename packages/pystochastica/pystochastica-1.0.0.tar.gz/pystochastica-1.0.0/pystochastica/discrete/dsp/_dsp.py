import matplotlib.pyplot as plt

class DiscreteStochasticProcess:
    """

    Summary
    -------
    A discrete stochastic process is an integer-indexed sequence
    of discrete random variables, X = (X_n)_{n : integer}. The 
    ``DiscreteStochasticProcess`` class is a general purpose class
    for initialising any discrete random process.
    
    - for each integer n, X_n is a RandVar type object
    
    """
    def __init__(self, time_steps: int) -> None:
        """Constructor method
        
        Parameters
        ----------
        time_steps : int
            the number of discrete random variables making up the process

        """
        self.time_steps: list[int] = time_steps

    def plot_process(self, **kwargs):
        """

        The ``plot_process`` methid is to be called after a process has been
        generated. Here, a process is understood as a list of RandVar objects.

        Parameters
        ----------
        stop : int, optional
            the number of random variables to sample in the discrete process 

        Returns
        -------
        plot : matplotlib.pyplot
            index of random variable vs sample of that random variable, 
            i.e., n -> (n, X_n)

        """
        # all processes are of RandVar objects, so they can be plotted in 2 dimensions
        process: list = self.process
        x = [i for i in range(self.time_steps)]
        y = [process[i].generate(1)[0] for i in range(self.time_steps)]
        try:
            stop: int = kwargs['stop']
        except KeyError:
            stop = self.time_steps
        x = x[:stop]
        y = y[:stop]

        plt.title(f"{self.title}")
        plt.xlabel("time steps")
        plt.ylabel("outcome")

        plt.plot(x, y, **kwargs)
        plt.show()
