# Instructions:

## Prerequisites:
    1. Python3 should be installed on the system.

## Running tests:
    1. Setup a virtual environment:
        For ubuntu:
            1. sudo apt install virtualenv
            2. virtualenv -p python3 name_of_environment
            3. To activate: source name_of_environment/bin/activate
        For windows:
            1.	pip install virtualenv
            2.	python -m venv <path for creating virtualenv>
            3.	To activate: <virtualenv path>\Scripts\activate

    2. Clone the repository: git clone https://github.com/Pirate2606/coding-platform.git
    3. Change the directory: cd coding-platform
    4. Install the requirements: pip install -r requirements.txt
    5. Run all tests at once using the following command: nose2

## To run the project locally, follow the following steps:
#### No need for step 1-4 if already done above
    1. Setup a virtual environment:
        For ubuntu:
            1. sudo apt install virtualenv
            2. virtualenv -p python3 name_of_environment
            3. To activate: source name_of_environment/bin/activate
        For windows:
            1.	pip install virtualenv
            2.	python -m venv <path for creating virtualenv>
            3.	To activate: <virtualenv path>\Scripts\activate

    2. Clone the repository: git clone https://github.com/Pirate2606/coding-platform.git
    3. Change the directory: cd coding-platform
    4. Install the requirements: pip install -r requirements.txt
    5. Generate OAuth client ID and Secret for Google.
    6. Place the client ID and secret for Google in "config.py" file.
    7. Create database: flask createdb
    8. Run the server: python3 app.py
    9. Open this link in browser: http://127.0.0.1:5000/
