from setuptools import setup, find_packages

setup(
    name='yfunc',
    version='1.0.1',
    description='a collection of some productive functions # b9af7f5cfbfe4446a646a6b24fd4590955816c25',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='yzjsswk',
    author_email='yzjsswk@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'clipboard',
        'pillow',
        'loguru',
    ],
)
