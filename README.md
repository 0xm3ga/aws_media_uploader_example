# AWS Media Uploader

## Project setup

### Virtual Environment

1. **Navigate to the project directory:**

   ```
   cd /path/to/project
   ```

2. **Create and activate the virtual environment:**

   - On **Linux/Mac**:

     ```
     python3 -m venv env
     source env/bin/activate
     ```

   - On **Windows**:

     ```
     py -m venv env
     .\env\Scripts\activate
     ```

3. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

4. **Exit the virtual environment:**

   ```
   deactivate
   ```

Remember to replace /path/to/project with the actual path to your project directory. This guide assumes that you have a requirements.txt file in your project directory. If not, you'll need to create one with the `pip freeze > requirements.txt` command while the virtual environment is activated and all necessary packages are installed.

### Pre-commit hooks

1. **Install pre-commit**: This can be achieved using pip, as shown below:

   ```bash
   pip install pre-commit
   ```

2. **Configure pre-commit hooks**: The configuration for pre-commit hooks is stored in the `.pre-commit-config.yaml` file, located in the root of the repository. The hooks included in this project are:

   - **Black**: A Python code formatter.
   - **Flake8**: A Python tool that bundles pep8, PyFlakes, and Ned Batchelder’s McCabe script for code linting.
   - **isort**: A utility to sort Python imports.
   - **mypy**: An optional static type checker for Python.
   - **Pytest**: Runs tests using the pytest framework.

3. **Install git hook scripts**: The following command installs the git hook scripts:

   ```bash
   pre-commit install
   ```

Upon successful installation, these pre-commit hooks will automatically format the code and check for issues each time a new commit is made, ensuring code quality and consistency throughout the development process.
