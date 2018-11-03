import codecs
import io
import os
import re
import sys
import webbrowser
import platform

try:
    from setuptools import setup
except:
    from distutils.core import setup


NAME = "quantaxis_webserver"
"""
名字，一般放你包的名字即可
"""
PACKAGES = ["QAWebServer"]
"""
包含的包，可以多个，这是一个列表
"""

DESCRIPTION = "QUANTAXIS:Quantitative Financial Strategy Framework"
KEYWORDS = ["quantaxis", "quant", "finance", "Backtest", 'Framework']
AUTHOR_EMAIL = "yutiansut@qq.com"
AUTHOR = 'yutiansut'
URL = "https://github.com/yutiansut/quantaxis_run"


LICENSE = "MIT"

setup(
    name=NAME,
    version='1.3.2',
    description=DESCRIPTION,
    long_description='automatic run quantaxis program',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['quantaxis_run>=1.3', 'quantaxis>=1.1.10.dev2'],
    entry_points={
        'console_scripts': [
            'quantaxis_webserver=QAWebServer.QA_Web:main',
            'quantaxis_webservice=QAWebServer.windowsservice:servicemain'
        ]
    },
    # install_requires=requirements,
    keywords=KEYWORDS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    include_package_data=True,
    zip_safe=True
)
