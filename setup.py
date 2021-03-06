# -*- coding: UTF-8 -*-
import os

import setuptools

setuptools.setup(
    name='TSI_Querier',
    version='0.3.1',
    keywords='',
    description='The querier designed for querying Time Series Insight data.',
    long_description=open(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'README.md'
        )
    ).read(),
    long_description_content_type = "text/markdown",
    author='Hanwei Wang',
    author_email='hanwei_wang_94@outlook.com',
    url = 'https://github.com/WHW-HAHA/TSI_Querier',
    license='MIT',
    install_requires=[

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
