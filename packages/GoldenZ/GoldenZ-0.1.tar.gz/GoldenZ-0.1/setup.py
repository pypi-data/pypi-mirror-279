from setuptools import setup, find_packages

setup(
    name='GoldenZ',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyminizip',
    ],
    entry_points={
        'console_scripts': [
            'goldenzip=goldenzip.core:golden_zip',
        ],
    },
    author='Golden_X',
    author_email='Golden@gmail.com',
    description='A tool for zipping files with password protection and sending the password via Telegram',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://t.me/RrrrrF',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
