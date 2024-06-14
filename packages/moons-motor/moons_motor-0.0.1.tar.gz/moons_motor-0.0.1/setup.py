from setuptools import setup, find_packages

setup(
    name="moons_motor",
    version="0.0.1",
    description="A simple motor control library for the Moons stepper motor driver",
    author="miroc99",
    packages=find_packages(),
    install_requires=["pyserial", "rich", "python-socketio"],
)
