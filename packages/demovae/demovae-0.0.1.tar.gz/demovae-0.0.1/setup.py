from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
        name = "demovae",
        version = "0.0.1",
        description = "A demographic-conditioned variational autoencoder for fMRI",
        long_description = "A demographic-conditioned variational autoencoder for fMRI distribution sampling, removal of confounds, and multi-site harmonization. Works with FC, ALFF, or ReHO data.",
        long_description_content_type="text/plain",
        url = "https://github.com/aorliche/demo-vae/",
        author = "Anton Orlichenko",
        author_email = "aorliche@gmail.com",
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: fMRI and imaging scientists",
            "Topic :: Generative Models :: Removal of Confounds",
            "License :: OSI approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            ],
        keywords = "fmri, vae, confounds",
        package_dir = {"src"},
        python_requires = ">=3.7, <4",
        install_requires = ["numpy", "scikit-learn", "torch"],
        )

