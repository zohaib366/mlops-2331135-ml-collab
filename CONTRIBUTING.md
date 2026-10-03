\# Contributing Guide



\## 1. Project Collaboration



This project follows a Git-based collaboration workflow for reproducible machine-learning development.



The repository uses protected long-lived branches and short-lived feature, data, experiment, and fix branches.



Direct pushes to `main`, `staging`, and `dev` are not allowed after the initial project import.



All changes to protected branches must be made through Pull Requests.



\---



\## 2. Branching Strategy



\### `main`



Production/release branch.



\* Contains released and reproducible versions of the ML project.

\* Changes are made only through Pull Requests.

\* Requires at least one approval.

\* Required CI checks must pass before merging.

\* Release versions are tagged on this branch.



\### `staging`



Release-candidate branch.



\* Contains changes being prepared for release.

\* Created from `main`.

\* Changes enter through Pull Requests.

\* Requires at least one approval.

\* Required CI checks must pass before merging into `main`.



\### `dev`



Integration branch.



\* Contains the integrated development work.

\* Created from `main`.

\* Feature, data, and completed experiment work is integrated here through Pull Requests.

\* Requires at least one approval.

\* Required CI checks must pass.



\### Feature branches



Used for production code and pipeline changes.



Naming:



```text

feat/<short-description>

```



Example:



```text

feat/model-training

feat/add-scaling

feat/update-training-pipeline

```



Feature branches are created from `dev` and merged back into `dev` through a Pull Request.



Delete the branch after it has been merged.



\### Data branches



Used for dataset changes and DVC-related work.



Naming:



```text

data/<short-description>

```



Example:



```text

data/update-wine-dataset

data/clean-duplicates

```



Data branches are created from `dev`.



Before pushing a data-related change, run:



```bash

dvc push

```



Then push the corresponding Git changes through a Pull Request into `dev`.



\### Experiment branches



Used for temporary model experiments and exploration.



Naming:



```text

exp/<member>-<idea>

```



Example:



```text

exp/shahid-random-forest

exp/zohaib-feature-scaling

```



Experiment branches:



\* Are short-lived.

\* Are created from `dev`.

\* Must not be merged directly into `dev`, `staging`, or `main`.

\* Should be rebased on the latest `dev` when necessary.

\* A successful experiment should be transferred to an appropriate `feat/` branch through cherry-picking or by reapplying the required changes.



\### Fix branches



Used for urgent production fixes.



Naming:



```text

fix/<short-description>

```



Example:



```text

fix/model-loading-error

```



Fix branches are created from `main`.



After review and testing, the fix is merged into `main` and then the corresponding change must also be brought back into `dev` to prevent the bug from returning in future development.



\---



\## 3. Commit Message Convention



This project uses \*\*Conventional Commits\*\*.



The general format is:



```text

<type>: <short description>

```



Common types include:



```text

feat:     new feature or production code change

fix:      bug fix

data:     dataset or DVC-related change

exp:      experiment or exploratory change

test:     adding or modifying tests

docs:     documentation changes

chore:    project/tooling/configuration changes

refactor: code restructuring without changing behavior

ci:       CI/CD workflow changes

```



Examples:



```text

feat: add feature scaling step

data: remove duplicate rows

exp: try random forest with max\_depth 8

fix: correct model loading path

test: add training pipeline tests

docs: update project setup instructions

chore: configure pre-commit hooks

ci: add GitHub Actions workflow

```



Commit messages should be:



\* Short and descriptive.

\* Written in the imperative style where practical.

\* Focused on one logical change.



Avoid vague messages such as:



```text

update

changes

final

new code

stuff

```



\---



\## 4. Pull Request Rules



All changes to `dev`, `staging`, and `main` must go through Pull Requests.



Every Pull Request should:



1\. Have a clear title describing the change.

2\. Explain what was changed.

3\. Mention relevant testing performed.

4\. Pass the required CI checks.

5\. Receive at least one approval from another team member.



Team members should review each other's Pull Requests rather than approving their own work.



\---



\## 5. Protected Branches



The following branches are protected:



```text

main

staging

dev

```



Protected branches require:



\* Pull Request before merging.

\* At least one approval.

\* Required CI checks to pass once CI is configured.

\* Force pushes are blocked.



Direct pushes to protected branches are not permitted during normal development.



The initial project import in Phase 2 is the only planned direct push to `main`.



\---



\## 6. Merge Strategy



\### Decision: Squash Merge



This project uses \*\*Squash Merge\*\* for Pull Requests.



Squashing combines the commits from a Pull Request into a single clean commit on the target branch.



This keeps the history of the long-lived branches (`dev`, `staging`, and `main`) easier to read and understand.



Individual development branches may contain multiple commits while work is in progress, but the final Pull Request should be merged using \*\*Squash and Merge\*\*.



\---



\## 7. General Workflow



For normal feature development:



```text

dev

&#x20;│

&#x20;└── feat/<name>

&#x20;      │

&#x20;      ├── make changes

&#x20;      ├── test

&#x20;      ├── commit

&#x20;      └── push

&#x20;             │

&#x20;             ▼

&#x20;            PR

&#x20;             │

&#x20;       teammate review

&#x20;             │

&#x20;        CI passes

&#x20;             │

&#x20;             ▼

&#x20;            dev

```



For a release:



```text

dev

&#x20;│

&#x20;▼

staging

&#x20;│

&#x20;▼

main

&#x20;│

&#x20;▼

release tag

```



For dataset changes:



```text

dev

&#x20;│

&#x20;└── data/<name>

&#x20;      │

&#x20;      ├── modify dataset

&#x20;      ├── dvc add / update

&#x20;      ├── dvc push

&#x20;      ├── git commit

&#x20;      └── PR → dev

```



For experiments:



```text

dev

&#x20;│

&#x20;└── exp/<member>-<idea>

&#x20;         │

&#x20;         └── experiment

&#x20;               │

&#x20;               └── successful result

&#x20;                      ↓

&#x20;                feat/<name>

```



\---



\## 8. Reproducibility



Changes affecting experiments, models, or datasets should preserve reproducibility.



Where applicable, record:



\* Git commit/version.

\* Dataset/DVC version.

\* Configuration/parameters.

\* Python dependency environment.

\* Random seed.

\* Model version.



The goal is that another team member can reproduce the same result from the repository.



