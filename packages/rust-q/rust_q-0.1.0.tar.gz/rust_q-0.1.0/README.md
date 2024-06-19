# Rust Q Learning with python bindings

This library is an implementation of Q learning, with containing python bindings.

# Installation

Build the repository with maturin:
```
maturin build -r --strip
```

Alternatively, you can also download the `.whl` file from the releases instead of building it yourself
Install the wheel using pip:
```
pip install target/wheels/rust_q-0.1.0-cp37-abi3-manylinux_2_34_x86_64.whl
```
