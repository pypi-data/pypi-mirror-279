from setuptools import setup, find_packages

def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content

setup(
    name='mjob',
    version='1.2.0',
    author='sirui.li',
    author_email='sirui.li@timekettle.co',
    packages=find_packages(include=['mjob']),
    entry_points={'console_scripts': ['mjob=mjob.mjob:main']},
    description='Perform parallel tasks based on a given file list',
    long_description=readme(),
    long_description_content_type='text/markdown',
    keywords='multi',
    install_requires=["tqdm"],
    url='https://github.com/timekettle/mjob',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    license='Apache License 2.0',
)
