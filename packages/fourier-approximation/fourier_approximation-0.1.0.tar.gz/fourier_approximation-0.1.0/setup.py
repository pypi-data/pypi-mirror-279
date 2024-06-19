from setuptools import setup, find_packages

setup(
    name='fourier_approximation',
    version='0.1.0',
    description='A package to approximate Fourier transforms',
    author='Lilian-Mo',
    author_email='ignifin@gmail.com',
    url='https://github.com/Lilian-Mo/fourier_approximation',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
