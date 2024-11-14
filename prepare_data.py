import pandas as pd
import os.path

# make sure the file is closed or not exist before running this program
input_signup_path = "signup_test_data.xlsx" 
input_login_path = "login_test_data.xlsx" 

updating_time = "101"
if os.path.isfile(input_signup_path):
    df = pd.read_excel(input_signup_path)
    if not pd.isnull(df.at[2, "Phone"]):
        phone = df.at[2, "Phone"]
        updating_time = str(phone % 1000 + 1)

# Create a dictionary for the test data
signup_test_data = {
    "FirstName": ["Gia Khiem", "Same", "Same", "Same", "Different"],
    "LastName": ["Dep Trai", "Phone", "Email", "PhoneAndEmail", "User"],
    "Phone": [
        "1111111" + updating_time,
        "1111111" + updating_time,
        "3333333" + updating_time,
        "1111111" + updating_time,
        "5555555" + updating_time,
    ],
    "Email": [
        "giakhiem.deptrai" + updating_time + "@example.com",
        "different.email" + updating_time + "@example.com",
        "giakhiem.deptrai" + updating_time + "@example.com",
        "giakhiem.deptrai" + updating_time + "@example.com",
        "different.user" + updating_time + "@example.com"
    ],
    "Password": [
        "CorrectPassword!" + updating_time, 
        "CannotCreate!" + updating_time, 
        "CannotCreate!" + updating_time, 
        "CannotCreate!" + updating_time, 
        "CorrectPassword!" + updating_time
    ],
    "Country": ["Japan", "United States", "Viet Nam", "China", "Russia"],
    "Expect": ["Successful", "Already Exist", "Already Exist", "Already Exist", "Already Exist"]
}

login_test_data = {
    "Email": [
        "giakhiem.deptrai" + updating_time + "@example.com",
        "not.existing.email" + updating_time + "@example.com",
        "gia.khiem" + updating_time + "@example.com",
        "different.user" + updating_time + "@example.com",
        "khiem140302@gmail.com"
    ],
    "Password": [
        "CorrectPassword!" + updating_time, 
        "CorrectPassword!" + updating_time, 
        "WrongPassword!" + updating_time, 
        "CorrectPassword!" + updating_time,
        "okeokeoke"
    ],
    "Expect": ["Unactivated", "Un signed up yet", "Wrong password", "Unactivated", "Successful"]
}

# Convert the dictionary into a DataFrame
df = pd.DataFrame(signup_test_data)
# Save the DataFrame to an Excel file
df.to_excel(input_signup_path, index=False)

# Convert the dictionary into a DataFrame
df = pd.DataFrame(login_test_data)
# Save the DataFrame to an Excel file
df.to_excel(input_login_path, index=False)
