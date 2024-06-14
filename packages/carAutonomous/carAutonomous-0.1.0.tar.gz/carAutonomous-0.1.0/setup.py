from setuptools import setup, find_packages

setup(
    name="carAutonomous",  # 替换为您的包名
    version="0.1.0",
    author="ryueiki",
    author_email="s2122056@stu.musashino-u.ac.jp",
    description="A simple example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/eiki7/carAutonomous",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'myapp=carAutonomous.app:main',
        ],
    },
)
