from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='crawl-bot',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'scrapy',
    ],
    entry_points={
        'console_scripts': [
            'run_spider=core.run_spider:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
