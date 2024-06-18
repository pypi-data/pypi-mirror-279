	
from setuptools import setup, find_packages

VERSION = "1.0.0"

def desc():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name='spicy-chat-ai',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description_content_type='text/markdown',
    author='Pandora',
    author_email='kafaatmadi@gmail.com',
    url="https://github.com/DeoDorqnt387/UNOFFICIAL-SpicyChat-API",
    description='spicychat api',
    long_description=desc(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'urllib3'
    ],
    keywords=['figgs', 'figgs.ai', 'figgsai api', 'figgs ai'],
    entry_points={
        "console_scripts": [
            "spicy=spicy.spicy:main"
        ]
    },
    python_requires='>=3.9',
)