## Description ##

This is the repository for the task on virtual environments. 
You can easily reproduce the results by running scripts locally if you **follow the instructions below**. Please notice that you will need the *requirements.txt* file to run the script, so do not delete it. 

This script has been run on the computer with the operating system **Ubuntu 22.04.1 LTS**.
Python version was Python **3.10.6**.

## Installation and usage ##

- **Python 3.10 installation**


To install Python3.10 on Ubuntu, you can follow the instructions on the [website](https://computingforgeeks.com/how-to-install-python-on-ubuntu-linux-system/)  and make python3.10 the main python version on your system. If you would like to use python3.10 in virtual environment, execute the following commands in command line:

`sudo apt update && sudo apt upgrade -y`

`sudo apt install software-properties-common -y`

`sudo add-apt-repository ppa:deadsnakes/ppa`

`sudo apt install python3.10`

`sudo apt install python3.10-venv`

`sudo apt install python3.10-pip`

`sudo apt install python3.10-distutils`

- **Virtual environment setting**

After python3.10 is installed, you should **create the virtual environment** by executing the following command in command line:

`python3.10 -m venv environment`

*Please note that your virtual environment should use python3.10.*

After this step is done, you should **activate the virtual environment** by executing the following command in command line:

`source environment/bin/activate`

After this step please **upload the dependencies** from file *requirements.txt* by executing the following command in command line:

`pip install -r requirements.txt`
  
- **Script running**
 
Finally, to **run the script** you should execute the following command in command line:

`python3 pain.py`

To **deactivate** the virtual environment you should execute the following command in command line:

`deactivate`


**Please contact the repository author if anything goes wrong.**