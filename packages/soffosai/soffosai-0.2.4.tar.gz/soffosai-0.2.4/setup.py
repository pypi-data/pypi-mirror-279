from setuptools import setup, find_packages

setup(
    name = "soffosai",
    version = "0.2.4",
    author = "Soffosai",
    author_email = "Soffos@soffos.ai",
    description = "A Python software development kit for using Soffos AI's APIs.",
    packages = find_packages(),
    package_data={'soffosai': ['*']},
    include_package_data=True,
)