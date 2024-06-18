from setuptools import setup

setup(
    name='trueloss',
    version='0.1.1',
    author='Siddique Abusaleh',
    author_email='trueloss.py@gmail.com',
    description='trueloss gives out the base loss for a keras neural network',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/trueloss/trueloss',
    py_modules=['trueloss'],
    install_requires=[
        'tensorflow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
