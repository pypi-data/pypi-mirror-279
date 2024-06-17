from setuptools import setup, find_packages

with open("README.rst", encoding="UTF-8") as f:
    readme = f.read()
    setup(
        name="ctxcli",
        version="0.1.0",
        description="CLI Tools for Amdocs ConnectX",
        long_description=readme,
        author="Amdocs ConnectX",
        author_email="roey@benamotz.com",
        packages=find_packages("src"),
        package_dir={"": "src"},
        install_requires=[],
        entry_points={
            "console_scripts": "cxcli=cxcli.cli:main",
        },
    )
