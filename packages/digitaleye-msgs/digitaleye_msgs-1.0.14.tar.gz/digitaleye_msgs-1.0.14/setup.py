import setuptools

setuptools.setup(
    name="digitaleye_msgs",
    version="1.0.14",
    author="Slink Tech",
    description="Python ROS Message for the PORTAL system",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["digitaleye_msgs"],
    package_dir={'':'.'},
    install_requires=[]
)
