from setuptools import setup, find_packages

setup(
    name="YWP",
    version="1.6.0",
    packages=find_packages(),
    install_requires=[
        "SpeechRecognition",
        "gtts",
        "pygame",
        "sounddevice",
        "pyaudio",
        "selenium",
        "tensorflow==2.16.1",
        "flask-cors",
        "flask",
        "nltk",
        "joblib",
        "tflearn",
        "setuptools",
        "wheel",
        "twine",
        "dill",
        "moviepy"
    ],
    author="Your Wanted Products",
    author_email="pbstzidr@ywp.freewebhostmost.com",
    description="A big Package has a lot of things",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
