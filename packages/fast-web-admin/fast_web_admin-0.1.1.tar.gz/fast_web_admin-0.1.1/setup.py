from setuptools import setup, find_packages

setup(
    name="fast-web-admin",
    version="0.1.1",
    keywords=("fastapi", "fastapi-admin"),
    description="FastAPI Admin Framework",
    author="buffalo",
    license="MIT",

    url="https://gitee.com/buffaloboy/fast-admin",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['fastapi', 'sqlalchemy', 'uvicorn'],
)
