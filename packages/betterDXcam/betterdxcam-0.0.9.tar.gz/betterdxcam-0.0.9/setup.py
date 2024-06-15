from setuptools import find_packages, setup

VERSION = "0.0.9"

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="betterDXcam",
    version=VERSION,
    description = "A Python high-performance screenshot library for Windows use Desktop Duplication API",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/E1Bos/betterDXcam",
    author="E1Bos",
    license="MIT",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture"
    ],
    install_requires=["numpy", "comtypes"],
    extras_require={
        "cv2": ["opencv-python"],
    },
    python_requires=">=3.7",
    include_dirs=["betterdxcam"],
)