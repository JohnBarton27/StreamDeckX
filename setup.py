import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="streamdeckx",
    version="0.0.1",
    author="John Barton",
    author_email="john@mediayoucanfeel.com",
    description="A cross-platform Stream Deck controller and programmer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JohnBarton27/StreamDeckX",
    project_urls={
        "Bug Tracker": "https://mediayoucanfeel.atlassian.net/jira/software/c/projects/SDX/issues/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "streamdeckx"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)