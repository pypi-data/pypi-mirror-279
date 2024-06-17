from ..core import RandVarBase
import matplotlib.pyplot as plt

class RandVarSimulator:
    """
    
    Summary
    -------
    Simulator for random variables as initialised by the ``RandVar`` class.
    For any number of random variables, ``RandVarSimulator`` will plot

    - their pdfs
    - their cdfs

    """
    FIGSIZE: tuple = (15, 9) # default figsize
    ITERATIONS: int = 1000 # default iterations

    def __init__(self, **kwargs) -> None:
        """Constructor method
        
        Parameters
        ----------
        iterations : int, optional
            custom number of iterations to simulate, default is 1000

        FIGSIZE : tuple, optional
            custom figure size (resolution), default is (15, 9)

        plt_kwargs : dict, optional
            custom parameters to pass to the .plot() method, e.g., color, width size, xticks rotation etc.

        """
        # get kwargs for configuration if any passed
        try:
            self.ITERATIONS: int = kwargs['iterations']
        except KeyError:
            pass 

        try:
            self.FIGSIZE: tuple = kwargs['FIGSIZE']
        except KeyError:
            pass

        try:
            self.plt_kwargs: dict = kwargs['plt_kwargs']
        except KeyError:
            pass

        try:
            self.plt_methods: dict = kwargs['plt_methods']
        except KeyError:
            pass

    def _plot(self, *randvars, **kwargs) -> None: # _plot since this method should not be called directly outside the RandVarSimulator class
        """RandVarSimulator's core plot method
        
        Parameters
        ----------
        randvars : list[RandVar]
            a list of ``RandVar`` objects

        title : str
            the title keyword for the plot

        plot_title : str
            the title keyword for each subplot

        xlabel : str
            label for x-axis

        ylabel : str
            label for y-axis

        plt_data : dict, keys x, y
            the data set to plot (x- and y-values)

        plt_type : str
            the type of plot (e.g., line, bar)
        
        plt_kwargs : dict
            extra parameters to pass to the ``matplotlib.pyplot.plot`` method, e.g., linestyle, color etc.
        
        Raises
        ------
        TypeError
            if not all elements in randvars are ``RandVar`` objects
        
        """
        if not all(isinstance(randvar, RandVarBase) for randvar in randvars):
            raise TypeError(f"not all arguments passed are {RandVarBase.__name__} objects")
        
        ncols: int = 1 if len(randvars) == 1 else 2
        nrows: int = sum(divmod(len(randvars), 2))
        fig, axs = plt.subplots(ncols=ncols, nrows=nrows, figsize=self.FIGSIZE, squeeze=False)

        # get data from kwargs
        title: str = kwargs['title']
        plot_title: str = kwargs['plot_title']
        xlabel: str = kwargs['xlabel']
        ylabel: str = kwargs['ylabel']
        plt_data: dict = kwargs['plt_data']
        plt_type: str = kwargs['plt_type']
        plt_kwargs: dict = kwargs['plt_kwargs']
        plt_methods: dict = kwargs['plt_methods']

        # generate subplots
        fig.suptitle(f"{title}")
        for i in range(nrows):
            for j in range(ncols):
                try:
                    index: int = ncols*i + j
                    randvar = randvars[index]
                    randvar_plt_data = plt_data[randvar]

                    x = randvar_plt_data['x']
                    y = randvar_plt_data['y']
                    axs[i, j].set_title(f"{plot_title} for {randvar.name}")
                    axs[i, j].set_xlabel(f"{xlabel}")
                    axs[i, j].set_xticks(x)
                    axs[i, j].set_ylabel(f"{ylabel}")
                    for method, value in plt_methods.items():
                        if method == 'set_xticklabels':
                            labels = axs[i, j].get_xticklabels()
                            getattr(axs[i, j], method)(labels, **value) # e.g., {'set_xticks': {'rotation': 45, 'ha': 'right'}}
                        else:
                            getattr(axs[i, j], method)(**value) 
                    getattr(axs[i, j], f'{plt_type}')(x, y, **plt_kwargs)
                except IndexError:
                    axs[i, j].axis("off")

        plt.tight_layout()
        plt.show()

    def pdfs(self, *randvars):
        """
        
        Parameters
        ----------
        randvars : list[RandVar]
            a list of ``RandVar`` objects    
        
        """
        # generate plot data for pdf plots
        plt_data: dict = {}
        for randvar in randvars:
            plt_data[randvar] = {}
            rv_outcomes = {sample.value: 0 for sample in randvar.pspace}
            outcomes: list = randvar.generate(self.ITERATIONS)
            for outcome in outcomes:
                rv_outcomes[outcome] += 1
            
            rv_outcomes = dict(sorted(rv_outcomes.items())) # sorted by key
            plt_data[randvar]['x'] = list(rv_outcomes.keys())
            plt_data[randvar]['y'] = list(rv_outcomes.values())
            plt_type: str = 'bar'

        # optional parameters for decorating the plot, e.g., color, xtick rotation etc.
        try:
            plt_kwargs: dict = self.plt_kwargs
        except AttributeError:
            plt_kwargs: dict = {'width': 0.95} # default kwargs to pass

        try:
            plt_methods: dict = self.plt_methods
        except AttributeError:
            plt_methods: dict = {}

        iterations: int = self.ITERATIONS
        self._plot(*randvars, **{
            'title': f"Probability distributions for {', '.join([f'{rv.name}' for rv in randvars])}",
            'plot_title': f'Probability distribution(s) after {iterations = }',
            'xlabel': 'outcomes',
            'ylabel': 'frequency',
            'plt_data': plt_data,
            'plt_type': plt_type,
            'plt_kwargs': plt_kwargs,
            'plt_methods': plt_methods
            })

    def cdfs(self, *randvars):
        """
        
        Parameters
        ----------
        randvars : list[RandVar]
            a list of ``RandVar`` objects    
        
        """
        # generate plot data for cdf plots
        plt_data: dict = {}
        for randvar in randvars:
            plt_data[randvar] = {}
            x = sorted([sample.value for sample in randvar.pspace])
            y = [randvar.Prob(f'<= {val}') for val in x]
            plt_data[randvar]['x'] = x
            plt_data[randvar]['y'] = y 
            plt_type: str = 'plot'

        # optional parameters for decorating the plot, e.g., color, xtick rotation etc.
        try:
            plt_kwargs: dict = self.plt_kwargs
        except AttributeError:
            plt_kwargs: dict = {'c': 'r'} # default kwargs
            
        try:
            plt_methods: dict = self.plt_methods
        except AttributeError:
            plt_methods: dict = {}

        self._plot(*randvars, **{
            'title': f"Cumulative distribution for {', '.join([f'{rv.name}' for rv in randvars])}",
            'plot_title': 'Cumulative distribution(s)',
            'xlabel': 'outcomes',
            'ylabel': 'probability',
            'plt_data': plt_data,
            'plt_type': plt_type,
            'plt_kwargs': plt_kwargs,
            'plt_methods': plt_methods
            })



