# VKernelRS

This project aims to provide a Rust implementation for a very basic filesystem and other kernel utilities
to be used in high performance virtual machines. This project is aimed at training large number of agents
in a isolated environment without relying on too slow virtual machines/containerization which are not well
suited for this kind of workloads.

# Features

- [x] Basic filesystem implementation
- [x] Basic terminal emulation
- [ ] Improving the filesystem with permissions and other features
- [ ] A more involved terminal emulation
- [ ] Syscalls hook and redirection


# How to use

This project uses Rust with python binding using the `pyo3` crates. For the interop it also require to
install the following python library:
```sh
pip install maturin
```

To help with the development and quick testing we advise created a python virtual environment and install
this project in development mode:
```sh
python -m venv .venv
source .venv/bin/activate
maturin develop --features=pybinding
```

To build the package and install it in your python environment:
```sh
maturin build --release --features=pybinding
pip install target/wheels/vkernelrs-0.1.0-cp39-cp39-linux_x86_64.whl
```

