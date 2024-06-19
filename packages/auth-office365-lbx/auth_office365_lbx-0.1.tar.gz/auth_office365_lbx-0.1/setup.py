from setuptools import setup, find_packages

setup(
    name='auth_office365_lbx',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'msal',
        'requests',
        'selenium',
        'webdriver-manager'
    ],
    description='Biblioteca para autenticação e verificação de grupos no Office 365',
    author='Cristiano P. Ferrari',
    author_email='boxferrari@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
