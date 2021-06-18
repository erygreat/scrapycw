from setuptools import setup, find_packages

version = open("scrapycw/VERSION").read()

setup(
    name='scrapycw',
    version=version,
    description="一个web监控scrapy的工具",
    long_description="""
        一个通过web监控和操作scrapy爬虫程序的监控工具。可以通过该工具启动、关闭、操作爬虫程序，也可以通过他观察爬虫的运行情况
    """,
    install_requires=[
        "Django==3.1.12",
        'Scrapy>=1.0',
        "psutil>=5.0.0",
        'pytest',
        'nanoid>=2.0.0',
        'request>=2.22.0',
    ],
    entry_points={
        "console_scripts": [
            "scrapycw = scrapycw.cmdline:execute",
        ],
    },
    include_package_data=True,
    packages=find_packages(exclude=('tests', 'tests.*')),
    author='erygreat',
    author_email='ery991172821@gmail.com',
    keywords='scrapy web monitor',
    url='https://github.com/erygreat/scrapycw',
    license="BSD",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Framework :: Django :: 3.0",
        "License :: OSI Approved :: Python Software Foundation License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
    ],
)
