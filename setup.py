from setuptools import setup, find_packages

version = open("scrapycw/VERSION").read()

setup(
    name='scrapycw',
    version=version,
    description="一个web监控scrapy的工具",
    long_description="""
        Scrapycw是一个Scrapy监控程序，你可以通过命令行或者web服务的方式监控Scrapy爬虫运行情况，以及进行运行爬虫等常用操作。
    """,
    install_requires=[
        "django-apscheduler>=0.5.2",
        "Django==3.1.12",
        'Scrapy>=1.0',
        "psutil>=5.0.0",
        'pytest',
        'nanoid>=2.0.0',
        'requests>=2.22.0',
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
    keywords='Scrapy Web Monitor',
    url='https://github.com/erygreat/scrapycw',
    license="BSD",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Framework :: Django :: 3.1",
        "Framework :: Pytest",
        "Framework :: Scrapy",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3"
    ],
)
