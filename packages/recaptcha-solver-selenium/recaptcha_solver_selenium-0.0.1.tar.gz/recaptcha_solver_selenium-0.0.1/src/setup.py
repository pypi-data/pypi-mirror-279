from setuptools import setup, find_packages

setup(
    name='recaptcha-solver-selenium',
    version='0.1',
    description='Solves reCAPTCHA challenges using Selenium WebDriver',
    long_description='A module to solve reCAPTCHA challenges on webpages using Selenium WebDriver.',
    author='Gabriel Foloni',
    url='https://github.com/folonidev/recaptcha-solver-selenium',
    packages=find_packages(),
    install_requires=[
        'pydub',
        'speechrecognition',
        'requests',
        'selenium',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
