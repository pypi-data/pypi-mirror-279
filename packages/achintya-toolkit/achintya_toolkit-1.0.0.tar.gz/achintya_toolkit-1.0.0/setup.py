from setuptools import setup, find_packages

setup(
    name='achintya_toolkit',
    version='1.0.0',
    packages=find_packages(),
    install_requires=['cv2', 'imghdr']
)

#python setup.py sdist bdist_wheel
#twine upload dist/*