from setuptools import setup, find_namespace_packages

with open('./README.md', 'r') as fh:
    long_description = fh.read()

with open('./requirements.txt', 'r') as fh:
    requirements = fh.readlines()

setup(
    name='planqk-service-sdk',
    version="1.3.12",
    author='Anaqor AG',
    author_email='info@anaqor.io',
    url='https://docs.platform.planqk.de/sdk-reference.html',
    description='Python SDK to execute PlanQK Managed Services.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_namespace_packages(include=['planqk', 'planqk.*']),
    license='apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    python_requires='>=3.9',
)
