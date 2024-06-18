"""
setup.py
"""
import io
from setuptools import setup, find_packages

def read(file_path):
    """
    Args:
        file_path (_type_):

    Returns:
        _type_:
    """
    with io.open(file_path, mode='r', encoding='utf-8') as f:
        return f.read()

setup(
    name='starlyng_server_management',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-mock==3.14.0',
            'pylint==3.2.2',
            'twine',
            'wheel',
        ],
    },
    entry_points={
        'console_scripts': [
            'server_management = server_management.__main__:main',
        ],
    },
    author='Justin Sherwood',
    author_email='justin@sherwood.fm',
    description='This project manages servers by rebooting using BCM due to crashes.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/starlyngapp/server-management',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
