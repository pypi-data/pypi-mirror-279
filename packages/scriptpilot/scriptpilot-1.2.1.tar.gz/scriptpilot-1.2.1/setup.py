from setuptools import setup, find_packages

setup(
    name="scriptpilot",
    version="1.2.1",
    description="A tool to manage the execution of multiple Python scripts.",
    long_description="""
        ScriptPilot is designed to manage the execution of multiple Python scripts based on their status 
        defined in a text file named 'sp_on_board.txt'. ScriptPilot provides functionalities to start, stop, 
        and monitor these scripts. It ensures that scripts are not duplicated and manages their lifecycle 
        efficiently.
    """,
    long_description_content_type="text/markdown",
    author="Javer Valino",
    url="https://github.com/yourusername/scriptpilot",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "psutil"
    ],
    entry_points={
        'console_scripts': [
            'scriptpilot=scriptpilot.__main__:main',  # Adjust as needed to your main script
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
