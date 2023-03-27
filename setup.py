import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='servis',
    version='0.0.1',
    packages=setuptools.find_packages(),
    include_package_data=True,
    long_description=long_description,
    description="Servis - a tool for drawing time series plots",
    author='Antmicro Ltd.',
    author_email='contact@antmicro.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'plotext==5.0.2'
    ],
    extras_require={
        'bokeh': [
            'bokeh==2.4.3'
        ],
        'matplotlib': [
            'matplotlib==3.6.1'
        ]
    },
    entry_points={
        'console_scripts': [
            'servis = servis.__main__:main'
        ]
    }
)
