# PyBuild

A Continuous Integration (CI) build system, testing all configurations where a TargetLink model is used.

## General Information about Pybuild

- PyBuild is fast.
  - More parallelization of jobs in the CI system makes it faster.
  - Code generation is moved to the developer's PC.
  - Code generation is done once for all projects using pre-processor directives.
  - C code reviews are now possible in Gerrit.
- PyBuild adds signal consistency checks.
- Unit tests of the build system are introduced.
  - Its quality is assured.
- PyBuild creates new variable classes with unique code decorations.
  - Post-processing C code is not necessary.
  - ASIL-classed variables get declared at the source.
  - Memory can be optimized at compilation through short addressing different variable classes.
  - The same models can be used in more than two different suppliers, for instance, SPA2's Core System Platform (CSP).
  - PyBuild fixes incorrect handling of NVM variables.

## Project Structure

- `docs/`: This directory holds all the extra documentation about the project.

- `playbooks/`: Directory where we keep Ansible playbooks that are executed in the jobs we use in this project.

- `pybuild/`: Main directory of the project. All the application source code is kept here. It is divided into different Python modules:
  - `interface/`
  - `lib/`
  - `zone_controller/`

Also, we keep `static_code/` and `templates/` directories with useful `.c`, `.h`, and `.html` files.

- `tests/`: Directory where we keep the unit tests for our application source code. The tests are structured in a similar way to what we have inside the `pybuild/` directory. Tests for the `interface`, `lib`, and `zone_controller` modules are split into `tests/interface/`, `tests/lib/`, and `tests/zone_controller/`, respectively. Other tests are kept inside the `tests/pybuild/` directory.

- `zuul.d/`: Directory where we keep our Zuul jobs.

## How to use Pybuild

## Contributing

We would love to see you contribute to this project. No matter if it is fixing a bug, adding some tests, improving documentation, or implementing new features. See our [contribution guidelines](./CONTRIBUTING.md) so you can have a better understanding of the whole process.

## Code of Conduct

We are trying to create a healthy community that thrives on the desire to improve, learn, and share knowledge. See our [code of conduct guidelines](./CODE_OF_CONDUCT.md) to check our behavioral rules on this project.
