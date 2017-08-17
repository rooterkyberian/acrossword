from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='acrossword',
    version='0.1',
    description='crossword generator',
    long_description=readme(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment :: Puzzle Games',
    ],
    keywords='crossword',
    url='http://github.com/rooterkyberian/acrossword',
    author='Maciej "RooTer" Urbański',
    author_email='rooter@kyberian.net',
    license='MIT',
    packages=['acrossword'],
    package_dir={'acrossword': 'src/acrossword'},
    install_requires=[
        'numpy',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    include_package_data=True,
    zip_safe=False
)
