from distutils.core import setup
from setuptools import find_packages

setup(
        name="carpet",
        version="0.0.2",
        url="https://github.com/alvaroabascar/carpet",
        license='MIT',
        author="Álvaro Abella",
        author_email="alvaroabascar@gmail.com",
        description="Library to create classes usable in 'with' blocks.",
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Programming Language :: Python :: 3.4'
                     ],
        packages=find_packages(exclude=['htmlcov', 'test']),
        install_requires=[],
        keywords="with context temporal file files temp tmp"
)
