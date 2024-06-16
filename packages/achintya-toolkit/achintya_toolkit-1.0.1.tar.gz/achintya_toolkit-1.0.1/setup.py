from setuptools import setup, find_packages

setup(

    name='achintya_toolkit',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'opencv-python',  # for cv2
        'imghdr',        # for imghdr (though it's part of the standard library, no need to list)
    ],
    author='Achintya Varshneya',
    author_email='achintya.varshneya@gmail.com'

    )

#python setup.py sdist bdist_wheel
#twine upload dist/*