from setuptools import setup, find_packages

setup(
    name='vital-agent-template',
    version='0.1.0',
    author='Marc Hadfield',
    author_email='marc@vital.ai',
    description='Vital Agent Template',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/vital-ai/vital-agent-template-python',
    packages=find_packages(exclude=["test"]),
    license='Apache License 2.0',
    install_requires=[
        'vital-ai-vitalsigns>=0.1.19',
        'PyYAML>=6.0.1'
    ],
    extras_require={
        'dev': [
            'wheel>=0.43.0'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
