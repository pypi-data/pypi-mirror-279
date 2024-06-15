from setuptools import setup, find_packages

setup(
    name="p_vs_np",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "sympy",
        "networkx",
        "opencv-python",
        # Add any other dependencies here
    ],
    entry_points={
        "console_scripts": [
            # Define command-line tools here if any
        ]
    },
    author="Drew Simpson",
    author_email="dsimps3@icloud.com",
    description="A library for P vs NP problems.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/p_vs_np",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
