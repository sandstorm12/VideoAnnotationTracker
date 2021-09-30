from setuptools import setup


def read_requirements(path='./requirements.txt'):
    with open(path, encoding='utf-8', errors='ignore') as file:
        install_requires = file.readlines()

    return install_requires


setup(
    name="VideoAnnotatorTracker",
    version="0.1.0",
    author="Hamid Mohammadi",
    author_email="sandstormeatwo@gmail.com",
    description="Demo for a potential video annotator with visual tracker",
    packages=['video_annotator_tracker'],
    scripts=[
        'vidtrack'
    ],
    install_requires=read_requirements()
)