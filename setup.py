from setuptools import setup, find_packages

setup(
    name="todo_tools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "rich>=10.0.0",
        "questionary>=1.10.0",
        "python-dateutil>=2.8.2",
        "prompt_toolkit>=3.0.0",
        "flask>=2.0.0"
    ],
    entry_points={
        'console_scripts': [
            'todo=todo_tools.__main__:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A command-line todo and task management tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/TODO_tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    package_data={
        'todo_tools': [
            'web/static/*',
        ],
    },
    include_package_data=True,
) 