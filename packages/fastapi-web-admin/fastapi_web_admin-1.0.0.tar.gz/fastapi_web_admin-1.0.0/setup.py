from setuptools import setup, find_packages

setup(
    name="fastapi-web-admin",
    version="1.0.0",
    keywords=("fastapi", "fastapi-admin"),
    description="FastAPI Admin Framework",
    long_description="FastAPI Admin Framework 快速构建FastAPI工程",
    author="buffalo",
    license="MIT",

    url="https://gitee.com/buffaloboy/fast-admin",

    # 需要打包的内容
    packages=find_packages(where=".", exclude=(), include=("*",)),
    include_package_data=True,
    package_data={"": ["*.*"]},
    exclude_package_data={"": ["*.pyc"]},

    platforms="any",
    install_requires=['fastapi', 'sqlalchemy', 'uvicorn'],

    entry_points={
        'console_scripts': [
            "fastapi-admin=admins.commands:main"
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
