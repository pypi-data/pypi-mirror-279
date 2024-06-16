from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(

    name='achintya_toolkit',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        'opencv-python',  
    ],
    author='Achintya Varshneya',
    author_email='achintya.varshneya@gmail.com',
    description="This is your one-stop-shop for all the cool and handy code snippets you'll ever need to make ML and DL as easy as pie!",
    long_description=long_description,  
    long_description_content_type='text/markdown',
    url='https://github.com/Acva11235/achintya-toolkit'

    )

#python setup.py sdist bdist_wheel
#twine upload dist/*