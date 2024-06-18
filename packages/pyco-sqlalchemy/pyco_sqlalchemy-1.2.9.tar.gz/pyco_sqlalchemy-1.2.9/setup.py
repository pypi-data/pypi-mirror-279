import json
import os
import subprocess
from setuptools import setup
from pyco_sqlalchemy import __version__
from datetime import datetime

description = "Simple ORM BaseModel for Flask depends on SqlAlchemy"

CurGit = os.path.abspath(os.path.join(__file__, "..", ".git"))
print(CurGit, os.path.abspath(CurGit))
extra_pkg = dict()

try:
    with open("readme.md", "r") as fh:
        readme = fh.read()

    PublishAt = datetime.now().strftime("%Y-%m-%d %H:%M")
    readme = readme.replace("${PublishAt}", PublishAt, 1)
    readme = readme.replace("${PublishVersion}", __version__, 1)
    if os.path.exists(CurGit):
        ##; git rev-parse HEAD
        _resGitCommit = subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True
        )
        GitCommit = _resGitCommit.stdout.strip()
        readme = readme.replace("${GitCommit}", GitCommit, 1)
        print("GitCommit:", GitCommit)
        ##; git log -n 2 .
        _resGitDetail = subprocess.run(
            ["git", "log", "-n" "2"], capture_output=True, text=True
        )
        GitDetail = _resGitDetail.stdout.strip()
        # print("GitDetail:", GitDetail)
        readme = readme.replace("${GitDetail}", GitDetail, 1)
        extra_pkg.update(
            _Version=__version__,
            PublishAt=PublishAt,
            GitCommit=GitCommit,
            GitDetail=GitDetail,
        )

except Exception as e:
    readme = description

PYPI_DIST_META = dict(
    name="pyco_sqlalchemy",
    url="https://github.com/dodoru/pyco-sqlalchemy",
    license="MIT",
    version=__version__,
    author="Nico Ning",
    author_email="dodoru@foxmail.com",
    description=(description),
    long_description=readme,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    packages=["pyco_sqlalchemy"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "SQLAlchemy<=1.3.4",
        "Flask-SQLAlchemy<=2.4.0",
        "Flask<=1.0.3",
    ],
    platforms='any',
)

if extra_pkg:
    extra_msg = json.dumps(extra_pkg, indent=2, ensure_ascii=False)
    fp_extra = "_.release.json"
    with open(fp_extra, "w") as f2:
        f2.write(extra_msg)
    # PYPI_DIST_META["package_data"] = {
    #     "pyco_info.json": [fp_extra]
    # }

setup(**PYPI_DIST_META)
