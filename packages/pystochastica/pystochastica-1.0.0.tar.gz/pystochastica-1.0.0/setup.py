from setuptools import setup
from pystochastica import __version__

modules = [
    'pystochastica.discrete.core',
    'pystochastica.discrete.dsp',
    'pystochastica.discrete.optimisers',
    'pystochastica.discrete.samples',
    'pystochastica.discrete.simulations',
    'pystochastica.discrete.utils',
    'pystochastica.discrete.variables',
    'pystochastica.discrete.vectors'
]

if __name__ == '__main__':
    setup(
        name='pystochastica',
        description='An open source stochastic calculus library written in Python',
        url='https://github.com/KshkB/pystochastica/',
        author='Kowshik Bettadapura',
        author_email='k.bettad@gmail.com',
        packages=['pystochastica'] + modules,
        version=f'{__version__}',
        license='MIT'
    )