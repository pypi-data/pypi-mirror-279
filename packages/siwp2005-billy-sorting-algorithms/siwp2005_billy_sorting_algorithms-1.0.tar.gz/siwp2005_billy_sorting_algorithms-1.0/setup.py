from setuptools import setup, find_packages

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='siwp2005_billy_sorting_algorithms',
    version='1.0',
    description='A collection of sorting algorithms',
    long_description=long_description,
    long_description_content_type='text/x-rst', 
    url='https://github.com/mjayy77/Siwp-2005-billy-sort.git',
    author='Billy',
    author_email='billymj77@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
