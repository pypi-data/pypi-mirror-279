from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='filegram',
    version='1.0.1',
    packages=find_packages(),
    author='Fidal',
    author_email='mrfidal@proton.me',
    url='https://mrfidal.in/cyber-security/filegram',
    description='A package to send files to Telegram groups',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'filegram=filegram.send_files:main',
        ],
    },
    keywords='telegram files send',
)
