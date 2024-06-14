from setuptools import setup
from setuptools import find_packages
from humai_tools import __version__

setup(
    name='humai_tools',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'mercadopago',
        'requests',
        'unidecode',
        'pydantic',
        'python-dotenv',
        'pydantic-settings',
        'pytz'
    ],
    author="Humai Dev Team",
    author_email="mg@humai.com.ar",
    description="Internal tools for private usage.",
    long_description_content_type="text/markdown",
    long_description="Internal tools for private usage.",
    url="https://github.com/institutohumai/humai_internal_tools",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
    ],
)
