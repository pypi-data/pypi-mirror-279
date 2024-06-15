from setuptools import setup, find_packages

setup(
    name='gpt_memory',
    version='0.0.3',
    description='A GPT memory management library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yang Sun',
    author_email='yangsun.com@gmail.com',
    url='https://github.com/git4sun/gpt_memory',
    packages=find_packages(include=['gpt_memory', 'gpt_memory.*']),
    install_requires=[
        'sqlalchemy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
