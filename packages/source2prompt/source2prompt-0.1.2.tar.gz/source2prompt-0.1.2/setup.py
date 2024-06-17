from setuptools import setup, find_packages

setup(
    name='source2prompt',
    version='0.1.2',
    packages=find_packages(include=['source2prompt']),
    entry_points={
        'console_scripts': [
            's2p=source2prompt.s2p:main'
        ]
    },
    install_requires=[
        'chardet',
    ],
    author='IchigoHydrogen',
    description='A simple tool to convert source files to a single prompt file for LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/IchigoHydrogen/source2prompt',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    include_package_data=True,
)