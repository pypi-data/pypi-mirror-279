from setuptools import setup, find_packages

setup(
    name="spot2mp3",
    version="1.0.3",
    description="A CLI tool to download Spotify playlist/album tracks as mp3 files.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Oliver Huang",
    author_email="ohuang4131@gmail.com",
    url="https://github.com/gooosexe/spot2mp3",
    license="GPLv3",
    packages=find_packages(),
	package_data={"spot2mp3": ["data/*.json"]},
    classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'spot2mp3=spot2mp3.cli:main',
        ],
    },
)
