# PyStochastica

Ever wanted to study arbitrary, linear and non-linear transformations of random variables? 
PyStochastica is an open source Python library tailored for doing that! 

It leverages Python's `SymPy` computer algebra system to provide a computer algebra system for random variables
and vectors.

## Installation

The `pystochastica` library is hosted at `PyPi`, see [here](https://pypi...). Run the following command to install it locally.

    $ pip install pystochastica

Run the following code from command-line to find the current version number of the installation

    $ python3 -c "import pystochastica; print(pystochastica.__version__)"

## Tutorials

See jupyter notebooks, hosted at the following links, for guides on using `PyStochastica`.

- [Random variables tutorial - initialisation]() 
- [Random variables tutorial - forming combinations]()
- [Random vectors tutorial - initialisation]()
- [Random vectors tutorial - linear combinations]()
- [Discrete stochastic processes]()
- [Optimisers]()

## Version numbering convention

The `1.0.*` version number series contains the `pystochastica.discrete` package with core classes `RandVar` and `RandVec`. 
Note that updates with new optimisers and discrete processes should be reflected through incrementing the least significant digit in `1.0.*`.

The `1.*.x` version series contains major upgrades to `pystochastica.discrete` comprising the addition of new core classes. These might include 
a `RandMtrx` class for random matrices and a `RandTensor` class for random tensors in line with comments in the Contributions section below.
Note, e.g., that the `1.1.*` series would include wrappers on existing core classes, e.g., such as optimisers or discrete processes for 
random matrices and tensors.

The `2.*.*` version number series should include work on continuous random variables, hosted at a separate package site, `pystochastica.continuous`.
Then `2.x.*` and `2.*.x` version series label progress as above.

The `3.*.*` version number series is expected to contain classes linking the core classes in `pystochastica.discrete` and `pystochastica.continuous`.
These may form a wholly separate package, such as `pystochastica.mixed`, where mixtures of discrete and continuous random variables may be formed.

## Contributions

The following sections detail areas where contributions may be made to PyStochastica. 
These are only non-exhaustive suggestions.

### Random matrices and tensors

Random variables are, in a suitable sense, `0` dimensional. Vectors, being a list of variables, are `one` dimensional.
Conventionally, *covariant* vectors are type `(1, 0)` tensors while *contravariant* vectors are of type `(0, 1)`. 
Continuing this analogy, matrices are then `2` dimensional. As tensors, they are of type `(1, 1)`.

As of writing, in PyStochastica version `1.0`, packages for tensors of type `(0, 0)`, `(1, 0)` and `(0, 1)` have been written.
More generally, this contribution requests pystochastica packages for type `(m, n)` random tensors. 

### Discrete stochastic processes

#### Binary options

The Black-Scholes equation is a famous equation used in the valuation of options on instruments whose price varies continuously
in time. Accordingly, the value of these options are modelled by continuous time, stochastic processes. A *binary* option is a 
 simplified version of the more complicated options seen in the wild and therefore may be modellable as a discrete process. 

This contribution requests a package for simulating the value of binary options as a discrete stochastic process.

### Optimisers

#### The Kelly criterion

Like mean-variance optimisation, the Kelly criterion can be used as another means of optimising random vectors. 
This involves maximising the expectation of the *Kelly function*, being the logarithm of a suitable objective
function.

This contribution requests a class for implementing optimisation of random vectors through the Kelly criterion.

### Continuous variables package

This contribution requests a package for studying and simulating continuous random variables and vectors in analogy
with the discrete package. Moreover, the continuous package ought to be compatible with the discrete package in the 
sense that continuous and discrete random variables ought to be combined to create random variables of mixed type, i.e., 
both continuous and discrete.