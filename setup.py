from setuptools import setup

setup(
    name="choralcat",
    version="0.0.1",
    url="https://choralcat.org",
    install_requires=[
        "Django>=4,<5",
        "python-dotenv>=0.19,<1"
        # Dev dependencies, version shouldn't matter
        "mypy",
        "black",
        "django-stubs",
    ],
)
