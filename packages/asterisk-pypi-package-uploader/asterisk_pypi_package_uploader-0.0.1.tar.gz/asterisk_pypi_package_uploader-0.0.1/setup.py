from setuptools import setup, find_packages

setup(
    name='asterisk_pypi_package_uploader',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['tk', 'sv_ttk', 'os', 'shutil', 'subprocess', 'twine', 'build'],
    description='A simple GUI for uploading pypi packages.',
    author='TheYellowAstronaut',
    author_email='malli.advait01@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
    