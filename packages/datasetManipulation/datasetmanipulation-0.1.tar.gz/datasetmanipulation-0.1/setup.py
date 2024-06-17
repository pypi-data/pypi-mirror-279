from setuptools import setup, find_packages

setup(
    name='datasetManipulation',
    version='0.1',
    description='Naia Science dataset Manipulation utils',
    long_description='This package contains utils to download, merge and split datasets',
    long_description_content_type='text/markdown',
    author='Axelle Lorin for Naia Science',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=[
        'roboflow==0.2.29',
        'ultralytics==8.0.196',
        'pycocotools',
        'split-folders',
    ],
    entry_points={
        'console_scripts': ['getAndMergeDatasets=src.getAndMergeDatasets:main'],
    },
)