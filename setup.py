"""
Setuptools installation for HereGeocoder.
"""

from setuptools import setup, find_packages


setup(
    name='HereGeocoder',
    version='0.0.2',
    description='Get point address from X/Y and vice versa',
    packages=find_packages(),
    install_requires=[
        'requests',
    ]
)
