# -*- coding: UTF-8 -*-
import os

import setuptools

setuptools.setup(
    name='TSI_Querier',
    version='0.1.1',
    keywords='',
    description='The querier designed for querying Time Series Insight data from WBL Big Data Platform.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    long_description_content_type = "text/markdown",
    author='Hanwei Wang',
    author_email='hanwei_wang_94@outlook.com',
    url = 'https://github.com/WHW-HAHA/TSI_Querier',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    package_dir={"": "TSI_QUERIER"},
    packages=setuptools.find_packages(where="TSI_QUERIER"),
)
