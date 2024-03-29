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

DESCRIPTION = "QUANTAXIS WEBSERVER: WEBSERVER FOR QUANTAXIS"
KEYWORDS = ["quantaxis", "quant", "finance", "Backtest", 'Framework']
AUTHOR_EMAIL = "yutiansut@qq.com"
AUTHOR = 'yutiansut'
URL = "https://github.com/yutiansut/quantaxis_webserver"


LICENSE = "MIT"

setup(
    name=NAME,
    version='2.0.0',
    description=DESCRIPTION,
    long_description='quantaxis webserver',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    install_requires=['tornado>=6.1', 'qaenv', 'apscheduler',
                      'quantaxis>=1.7.0'],
    entry_points={
        'console_scripts': [
            'quantaxis_webserver=QAWebServer.QA_Web:main'
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
