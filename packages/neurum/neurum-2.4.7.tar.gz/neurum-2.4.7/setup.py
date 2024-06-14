from setuptools import setup, find_packages

classifiers = ['Development Status :: 2 - Pre-Alpha', 
               'Intended Audience :: Developers', 
               'Operating System :: MacOS :: MacOS X',
               'Operating System :: Microsoft :: Windows', 
               'Operating System :: Unix',  
               'License :: OSI Approved :: MIT License', 
               'Programming Language :: Python',]

setup(
    name= 'neurum', 
    version='2.4.7',
    description='A powerful multimodal AI sdk for python by Neurum Inc..',
    url='https://github.com/VanshShah1/notion',
    author='Vansh Shah', 
    author_email='vanshshah836@gmail.com',
    License='MIT', 
    classifiers=classifiers, 
    keywords='ai api sdk llm',
    packages=find_packages(),
    install_requires=['quickjs'],
)