# NextUtils

## Telemetry (cpp)

### Overview
This project integrates Python 3.12 with C++ code using `pybind11`. To ensure the project functions as intended, it is important to set up Python 3.12 correctly by installing it in the parent directory of the project. This setup ensures that the Python folder and the project folder are siblings.

### Prerequisites
- **Python 3.12** or higher
- **pybind11** library

### Installation

#### 1. Install Python 3.12

To ensure the paths and project configurations work properly, follow these steps to install Python 3.12 in the correct location:

#### For Windows:

1. **Download Python 3.12**:
   - Visit the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/).
   - Download the installer for Python 3.12 suitable for your operating system.

2. **Install Python in the Parent Directory**:
   - During the installation, select "Custom Installation".
   - Set the installation path to the parent directory of the project folder.
   - **Example**:
     ```
     C:\path\to\parent\project-folder
     ```
     Install Python in:
     ```
     C:\path\to\parent\python-folder
     ```
   - After installation, your directory structure should look like this:
     ```
     C:\path\to\parent\
         ├── python-folder\    (Python 3.12 installation)
         └── project-folder\   (Your project)
     ```

3. **Add Python to the System Path**:
   - Ensure you check the option to "Add Python to PATH" during the installation process. This allows Python to be accessed from the command line.

4. **Verify the Installation**:
   - Open Command Prompt and run `python --version`. This should output `Python 3.12.x`.

#### For Linux (e.g., Ubuntu):

1. **Install Python 3.12 using deadsnakes PPA**:
   Run the following commands in the terminal:
   ```
   sudo add-apt-repository ppa
   ppa sudo apt update sudo apt install python3.12/
   ```

2. **Verify the Installation**:
Run `python3.12 --version`. This should output `Python 3.12.x`.

#### 2. Install `pybind11`

   1. Open a terminal or command prompt.
   2. Navigate to the project directory:
   ```
   cd /path/to/parent/project-folder
   ```
   3. Install `pybind11` using `pip`:
   ```
   pip install pybind11 --target=/path/to/parent/project-folder/Lib/site-packages
   ```


#### 3. Copy Python DLL (Windows Only)

1. **Locate the Python DLL file**:
- Typically named `python3x.dll` (where `x` is the minor version number) in the Python installation directory:
  ```
  C:\path\to\parent\python-folder\DLLs\
  ```
2. **Copy the DLL file to the Executable Directory**:
- For example:
  ```
  C:\path\to\parent\project-folder\bin\
  ```

#### 4. Build and Run the Project

#### For Windows:

   **Build the Project**:
   Use Visual Studio or another build system of your choice to build the project.


#### For Linux:

1. **Build the Project**:
```
cd /path/to/parent/project-folder
mkdir build 
cd build 
cmake .. 
make
```

2. **Run the Executable**:
   ```
   cd ..
   ```
   Run `./my_executable_name`

3. **Notes**:
- Ensure the executable has execution permissions:
  ```
  chmod +x /path/to/parent/project-folder/build/my_executable_name
  ```

---

### Additional Notes
- Ensure all dependencies are installed correctly before building and running the project.
- If you encounter issues during installation or building, check the error messages and verify that all steps have been followed accurately.
- For more information and support, visit the [GitHub Issues](https://github.com/YourRepo/Issues) page of the project.

---


## PostgreSQL Setup Instructions

To support PostgreSQL in this project, follow the steps below:

### Step 1: Download and Install PostgreSQL

1. **Download PostgreSQL (version 15 or higher)**  
   - Visit the official PostgreSQL website: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
   - Choose the appropriate version for your OS (ensure you download version 15 or later).

2. **Install PostgreSQL**  
   Follow the installation steps based on your operating system:
   - **Windows**: Run the installer, select your installation directory, and proceed with the default components.
   - **macOS**: Use Homebrew:  
     ```bash
     brew install postgresql@15
     ```
   - **Linux**: Use your distribution's package manager. For example, on Ubuntu:  
     ```bash
     sudo apt-get install postgresql-15
     ```

3. **Set a Password for the PostgreSQL User**  
   During installation, you will be prompted to set a password for the `postgres` user. Keep this information safe, as it will be needed later to set up the database connection.

### Step 2: Add PostgreSQL to the System Path

You need to add PostgreSQL’s `bin` directory to your system’s environment variables to ensure the tools (like `psql` and `pg_config`) can be accessed from the command line.

- **Windows**:  
  1. Right-click on "This PC" → **Properties** → **Advanced system settings** → **Environment Variables**.
  2. Under "System Variables", select **Path** and click **Edit**.
  3. Click **New**, then enter the path to the PostgreSQL `bin` folder (e.g., `C:\Program Files\PostgreSQL\15\bin`).
  4. Click **OK** to save the changes.

- **macOS/Linux**:  
  Add the following line to your `.bashrc` or `.zshrc` file:
  ```bash
  export PATH="/usr/local/pgsql/bin:$PATH"
   ```
### Step 3: Configure the Project with PostgreSQL

Ensure the project points to the correct PostgreSQL libraries and headers.

#### Set Up PostgreSQL in Visual Studio:

1. Open Visual Studio and right-click on your project in **Solution Explorer**.
2. Select **Properties**.
3. Go to **C/C++ → General → Additional #using Directories**.
4. Add the path to the PostgreSQL include directory (e.g., `C:\Program Files\PostgreSQL\15\bin`).

### Link Against `libpq`:

1. Under **Linker → Input → Additional Dependencies**, add `libpq.lib` to ensure the PostgreSQL client library is linked properly.

---

### Step 4: Update the Connection String

In the project source code in Config.h , update the PostgreSQL connection to use the correct port, username, and password. For example:

```cpp
    const std::string PASSWORD = "1234";
    const std::string POSTGRE_DB_NAME = "database";
```
### Step 5: Verify and Test

Once PostgreSQL is installed and configured:

1. Verify that the PostgreSQL server is running.
2. Ensure that the project builds correctly with the updated configurations.
3. Run the project to ensure that it can connect to the PostgreSQL database and perform read/write operations successfully.

## Configuration File (config.json):


**The config.json file contains important settings for the application. Please make sure to configure the file according to your requirements before running the application.**


Here are the details of the configuration options:


* database_types: This array contains the available database types. You can choose one type from the provided options, such as "PGSQL" or "SQLite", and set it as the value for the selectedDB attribute.


* selectedDB: Set this attribute to your chosen database type from the database_types array.


* PGSQL_password: Ensure to update the "PGSQL_password" attribute with the correct password for the PGSQL database on your local machine.


Please modify the config.json file accordingly to match your desired database settings, as well as provide the correct PGSQL password before running the application."


