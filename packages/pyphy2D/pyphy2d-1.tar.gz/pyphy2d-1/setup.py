from setuptools import setup, find_packages

setup(
    name='pyphy2D',
    version='1',
    author='Krishiv Goel',
    author_email='KrishivGoelXD@gmail.com',
    description='A 2D Rigid Body Physics Engine.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['pygame-ce'],
)