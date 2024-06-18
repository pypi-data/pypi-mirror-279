from setuptools import setup

setup(
    name='jbtsdk',
    description=u'SDK Jabuti Technologies',
    version='0.0.34',
    license='MIT License',
    author='Thales Araújo',
    install_requires=[
        "requests",
        "langchain",
        "langchain_community",
        "streamlit"],
)