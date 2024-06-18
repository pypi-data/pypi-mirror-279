from setuptools import setup

with open("README_DBUTILS.md", "r") as fh:
    long_description = fh.read()

setup_args = dict(
    name="dbutils3-gonzalo123",
    version="3.0.2",
    author="Gonzalo Ayuso",
    author_email="gonzalo123@gmail.com",
    description="psycopg3 db utils",
    long_description=long_description,
    license='MIT',
    long_description_content_type="text/markdown",
    keywords=['psycopg3'],
    url="https://github.com/gonzalo123/dbutils3",
    packages=['dbutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)

install_requires = [
    'psycopg>=3'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
