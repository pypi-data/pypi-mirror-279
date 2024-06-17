from setuptools import setup, find_packages

setup(
    name='crawl_bot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'scrapy',
    ],
    entry_points={
        'console_scripts': [
            'run_spider=crawl_bot.run_spider:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
