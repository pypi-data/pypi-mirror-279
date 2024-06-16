from setuptools import setup, find_packages

setup(
    name='asterisk-pypi-pack-uploader',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['sv_ttk', 'tk', 'twine', 'build'],
    description='A simple GUI for uploading packages to PyPi.',
    author='TheYellowAstronaut',
    author_email='malli.advait01@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
    