from setuptools import setup, find_packages

setup(
    name='bukalapak-scraper',
    version='0.1.0',
    description='A Python library to scrape product prices from Bukalapak.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/bukalapak-scraper',
    packages=find_packages(),
    install_requires=[
        'selenium',
        'beautifulsoup4',
        'webdriver-manager'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
