from setuptools import setup, find_packages

setup(
    name="fast-web-admin",
    version="0.1.2",
    keywords=("fastapi", "fastapi-admin"),
    description="FastAPI Admin Framework",
    author="buffalo",
    license="MIT",

    url="https://gitee.com/buffaloboy/fast-admin",
    packages=find_packages(where=".", exclude=(), include=("*",)),
    include_package_data=True,
    platforms="any",
    install_requires=['fastapi', 'sqlalchemy', 'uvicorn'],

    entry_points={
        'console_scripts': [
            "fastapi-admin=commands:main"
        ]
    },

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ]
)
