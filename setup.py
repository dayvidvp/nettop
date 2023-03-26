from setuptools import setup, find_packages

setup(
    name="nettop",
    version="0.1",
    packages=find_packages(),
    entry_points={"console_scripts": ["nettop = nettop:display_network_data"]},
    install_requires=["psutil", "rich"],
)
