"""
python setup.py sdist bdist_wheel
python -m twine upload dist/*
"""

import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zyh_24_06_17",
    version="5.0.0",
    author="zyh",
    author_email="zhuyihe@petail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",  # 你的项目地址，例如GitHub
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    # 添加依赖项，这里只是一个示例，你需要根据你的包实际依赖来修改
    install_requires=["scikit-learn==1.2.2", "joblib==1.4.2", "numpy==1.25.2"],
    include_package_data=True,
)
