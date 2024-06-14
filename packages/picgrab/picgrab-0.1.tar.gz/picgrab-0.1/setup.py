from setuptools import setup

setup(
    name='picgrab',
    version='0.1',
    py_modules=['picgrab'],
    author='Avinion',
    author_email='shizofrin@gmail.com',
    url='https://twitter.com/Lanaev0li',
    description='A script to download images from web pages',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='Avinion Group',
    entry_points={
        'console_scripts': [
            'picgrab=picgrab:main',
        ],
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tqdm'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
