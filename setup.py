# -*- coding: UTF-8 -*-
import os

import setuptools

setuptools.setup(
    name='WBL_BDP_TSI_Querier',
    version='0.0.1',
    scripts=['Python'],
    keywords='',
    description='The querier designed for querying Time Series Insight data from WBL Big Data Platform.',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.md'
        )
    ).read(),
    long_description_content_type = "text/markdown",
    author='LiuMao',
    author_email='hanwei_wang_94@outlook.com',
    packages=setuptools.find_packages(),
    url = '',
    license='MIT',
    install_requires=[]
)
