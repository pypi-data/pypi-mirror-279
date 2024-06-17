from setuptools import setup

if __name__ == "__main__":
    setup(
        name="real_robot",
        package_dir={"real_robot": "real_robot"},
        package_data={"real_robot": ["assets/**"]},
        exclude_package_data={"": ["*.convex.stl"]},
        extras_require={
        },
        zip_safe=False,
    )
