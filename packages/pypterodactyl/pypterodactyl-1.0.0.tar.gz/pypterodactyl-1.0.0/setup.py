from setuptools import setup, find_packages

long_description = """
A Python wrapper for Pterodactyl dashboards
"""

setup(
    name="pypterodactyl",
    version="1.0.0",
    author="kokofixcomputers",
    author_email="koko@kokofixcomputers.stio.studio",
    description="A Python wrapper for Pterodactyl dashboards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)