from setuptools import setup, find_packages

setup(

    name='achintya_toolkit',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'opencv-python',  # for cv2
    ],
    author='Achintya Varshneya',
    author_email='achintya.varshneya@gmail.com'

    )

#python setup.py sdist bdist_wheel
#twine upload dist/*