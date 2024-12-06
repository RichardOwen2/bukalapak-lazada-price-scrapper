from setuptools import setup, find_packages

setup(
    name="bukalapak-lazada-price-scrapper",
    version="0.2.0",
    description="A package for scraping product prices from Bukalapak and Lazada.",
    author="Richard Owen Hoan",
    author_email="richardowen2411@gmail.com",
    url="https://github.com/RichardOwen2/bukalapak-lazada-price-scrapper",  # Change to your GitHub repo
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
