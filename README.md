Banking System Application

Steps to Run the Application on Your System

Step 1: Check Python Version
Ensure you have Python 3.9.11 installed:
python --version
If you don't have Python 3.9.11, download and install it from python.org.


Step 2: Clone the Repository
Clone the repository to your local machine:
git clone https://github.com/Prashanthg01/banking_system.git


Step 3: Navigate to the Project Directory
get into the project directory:
cd banking_system


Step 4: Create a Virtual Environment
Create a virtual environment to manage dependencies:
python -m venv myenv


Step 5: Activate the Virtual Environment
Activate the virtual environment:

On Windows:
.\myenv\Scripts\activate

On macOS/Linux:
source myenv/bin/activate


Step 6: Install Requirements
Install the required packages:
pip install -r requirements.txt


Step 7: Set Up Environment Variables
Create a .env file in the root folder (banking_system) with the following content:

FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY="set_your_secret_key_here"
MONGO_URI=mongodb://localhost:27017/banking_system
JWT_SECRET_KEY="set_your_jwt_secret_key_here"
To set the JWT_SECRET_KEY, you can generate a key from this site.


Step 8: Install MongoDB Compass
Download and install MongoDB Compass from this link.
https://downloads.mongodb.com/compass/mongosh-2.2.6-win32-x64.zip


Step 9: Connect to MongoDB Compass
Open MongoDB Compass and connect using the following URI:
mongodb://localhost:27017


Step 10: Run the Application
Start the Flask application:
python run.py


Your application should now be running, and you can access it in your web browser.

How the Banking System Works:


Step 1: Register a Customer Account
Visit the following URL to register a customer account:
http://127.0.0.1:5000/banker/register_account


Step 2: Register a User Account
Visit the following URL to register a user account:
http://127.0.0.1:5000/auth/register
Note: When you register a user account, your role will be set to "customer" by default. This means you will have access to the customer dashboard upon login. If you want to access the banker dashboard, you will need to change your role to "banker" in MongoDB.

Step 3: Login to Your Account
Visit the following URL to log in to your account:
http://127.0.0.1:5000/auth/login
Upon successful login, you will be redirected to the specific dashboard based on your role.


Step 4: Deposit Money
Send a deposit request to the banker by visiting the following URL:
http://127.0.0.1:5000/transactions/deposit


Step 5: Withdraw Money
Send a withdrawal request to the banker by visiting the following URL:
http://127.0.0.1:5000/transactions/withdraw


Step 6: Check Your Balance
Visit the following URL to check your balance:
http://127.0.0.1:5000/customer/check_balance
Note: If you do not have a UPI ID, you will need to create one before checking your balance.


Step 7: Banker Dashboard
If you are logged into the banker dashboard based on your role, you will have the following capabilities:
Update Deposit and Withdraw Status: Change the status of deposit and withdrawal requests from pending to accepted or declined.
If a deposit is accepted, the requested amount will be added automatically.
If a withdrawal is accepted, the requested amount will be deducted automatically.
Manage Accounts:
Add new accounts.
Delete and edit existing accounts.
Access Transaction History: View the complete deposit and withdrawal history.

Further Improvements

1. The application uses basic error handling techniques, including try and except methods and an error log file.
2. No test cases are written. We can use pytest to write test cases.
3. There is no CI/CD pipeline to deploy and test the application when new code is pushed.
4. No OTP integration for security, but passwords and UPI IDs are saved in hashed format.