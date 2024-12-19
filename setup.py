from setuptools import setup, find_packages

setup(
    name="ecommerce-price-scraper",
    version="0.2.2",
    description="A package for scraping product prices from Bukalapak, Lazada, and your own custom e-commerce website.",
    author="Richard Owen Hoan",
    author_email="richardowen2411@gmail.com",
    url="https://github.com/RichardOwen2/ecommerce-price-scraper", 
    packages=find_packages(),
    install_requires=[
        'selenium',
        'webdriver-manager',
        'beautifulsoup4',
        'requests',  # Optional but good for other HTTP requests
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
