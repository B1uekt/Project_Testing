# Automated Browser Testing with Selenium and pytest

This project is designed for automated browser testing using Selenium and pytest. The following instructions guide you through setting up the environment, installing required dependencies, and running the test scripts.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the Selenium Environment](#setting-up-the-selenium-environment)
- [Running Tests with pytest](#running-tests-with-pytest)

---

## Prerequisites

To run this project, you need to have the following installed on your system:

1. **Python 3.x**: You can download Python from [python.org](https://www.python.org/downloads/).
2. **pip**: Python’s package installer, which usually comes with Python. Verify by running `pip --version` in your terminal.

---

## Setting Up the Selenium Environment

To use Selenium with `pytest`, follow the steps below to set up the environment.

### Step 1: Install WebDriver

Download browser-specific drivers: 
1. **Chrome**: You can download ChromeDriver from [(https://developer.chrome.com/docs/chromedriver/download/)](https://developer.chrome.com/docs/chromedriver/downloads)
2. **Firefox**: You can download  from ([https://developer.chrome.com/docs/chromedriver/download/](https://github.com/mozilla/geckodriver/releases))

### Step 2: Install Required Python Packages

To install Selenium and pytest, open your terminal and run:

```bash
pip install selenium pytest

```

---

## Running Tests with pytest 
Write the test scripts, then run the script by opening the terminal and run:

```bash
pytest test_login.py 
```
With test_login.py is a name of test file

To get even more detailed output, use the -v flag:

```bash
pytest -v test_login.py
```

For a more visual representation of the test results, you can generate HTML reports using the pytest-html plugin.

1. **Install pytest-html**
```bash
pip install pytest-html
```
2. **Run tests with HTML report generation**
```bash
pytest --html=report.html
```
The report.html file will be saved in the same directory as the test file
