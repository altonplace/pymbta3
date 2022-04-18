import setuptools
from distutils.core import setup

setup(
    name='pymbta3',
    version='0.0.4dev',
    packages=['pymbta3', ],
    license='MIT',
    author='Mike Anderson',
    author_emal='maanderson4@gmail.com',
    url='https://github.com/altonplace/pymbta3',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=['requests'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",

    ],
    keywords='mbta api',

)
