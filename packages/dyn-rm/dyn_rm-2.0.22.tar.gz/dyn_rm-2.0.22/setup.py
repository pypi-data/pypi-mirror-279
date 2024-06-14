from setuptools import setup, find_packages


setup(
    name='dyn_rm',
    version='2.0.22',
    description='A Modular Dynamic Resource Manager for Exploration',
    author='Dominik Huber',
    author_email='domi.huber@tum.de',
    url='https://gitlab.inria.fr/dynres/dyn-procs/dyn_rm',
    packages=find_packages(),
    install_requires=[
        # List any dependencies your package requires
        'pypmix',
        'pyyaml',
        'numpy'
    ],
)
