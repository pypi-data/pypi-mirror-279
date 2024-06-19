from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='dalab',  # required
    version='2024.6.18.17',
    description='dalab: A Data Assimilation Laboratory in Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu',
    author_email='fengzhu@ucar.edu',
    url='https://github.com/fzhu2e/dalab',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    zip_safe=False,
    keywords='Data Assimilation',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'netCDF4',
        'xarray',
        'dask',
        'nc-time-axis',
        'colorama',
        'tqdm',
        'x4c',
        'f90nml',
    ],
)
