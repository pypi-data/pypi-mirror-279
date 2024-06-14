from setuptools import setup, find_packages

setup(
name='ExtPenPy',
version='1.3',
author='Anas Shlool, MalikTawfiq, Yanal Abuseini',
author_email='anasshlool11@gmail.com',
description='ExtPenPy is a tool that will help you finalizing your recon phase faster.',
packages=["ExtPenPy"],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
entry_points={
        'console_scripts': [
            'ExtPenPy = ExtPenPy.ExtPenPy:main',
        ]
    },
python_requires='>=3.10',
install_requires=[
    "androguard",
    "apk2java",
    "dnspython",
    "python-whois",
    "requests",
    "whois",
    "webdriver-manager",
    "Selenium",
    "more-itertools"

]

,url="https://github.com/maliktawfiq/ExtPenPy",
)