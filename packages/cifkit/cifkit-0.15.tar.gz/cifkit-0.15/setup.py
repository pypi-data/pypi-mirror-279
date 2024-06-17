from setuptools import setup, find_packages

setup(
    name="cifkit",
    version="0.15",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[],  # List your dependencies here
)


"""
python setup.py sdist bdist_wheel
twine upload dist/*         
"""