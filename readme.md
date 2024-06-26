## Running locally

### Clone the project

Clone the repository using the following command:

```bash
git clone https://github.com/MateusGurgel/fast-api-template.git
```

### Access the project directory

Navigate to the project directory with the command:

```bash
cd fast-api-template
```

### Create a virtual environment

Create a virtual environment using Python's `venv`:

```bash
python -m venv venv
```

### Activate the virtual environment

#### On Windows:

To activate the virtual environment on Windows, use the command:

```bash
.\venv\Scripts\activate
```

#### On Linux:

To activate the virtual environment on Linux, use the command:

```bash
source ./venv/bin/activate
```

### Start the template

You can start the template in two ways:

1. **Running the main file:**

   ```bash
   python main.py
   ```

2. **Using Uvicorn:**

   ```bash
   uvicorn main:app --reload
   ```

Now you're ready to start working with the project locally 😁.


## TODO

Make the query builder affect only search_functions with a @tag on it

Use another lib for hashing

Use random salts for every user

Implement Logging on the aplication
