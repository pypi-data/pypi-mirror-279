from setuptools import setup, find_packages

setup(
    name='betterjsdc',
    version='1.0.0',
    description='A better interface for transforming dataclasses to and from dictionaries.',
    author='Benjamin Brecher',
    author_email='brecherbenjamin@gmail.com',
    url='https://github.com/boboben1/jsondataclass',
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)