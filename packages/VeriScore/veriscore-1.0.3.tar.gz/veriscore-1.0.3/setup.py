from setuptools import setup, find_packages

setup(
   name="VeriScore",
   version="1.0.3",
   packages=find_packages(),
   install_requires=[
       #'requests', 'numpy'
      'spacy',
      'openai',
      'anthropic',
      'tiktoken',
      'tqdm',
   ],
   description="Pip package for Verifact",
   long_description=open('README.md').read(),
   long_description_content_type="text/markdown",
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   python_requires='>=3.9',
)
