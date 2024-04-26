import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import random
import string
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver import Edge



def second_mail_creation_procedure():
    emails = []
    # Create a connection object to the DB using credentials
    db = mysql.connector.connect(
        host="eivor.aserv.co.za",
        user="bluenskg_info",
        password="mmDev2024%%",
        database="bluenskg_student_space"
        )

    cursor = db.cursor()
    # Fetch the rows where second_mail is not set
    cursor.execute("SELECT id, name, surname FROM applicants WHERE second_mail IS NULL")
    rows = cursor.fetchall()


    for row in rows:
        id, name, surname = row
        counter = 0
        while True:
            email = f"{name}.{surname}{str(counter) if counter > 0 else ''}@bluenroll.co.za"
            cursor.execute("SELECT COUNT(*) FROM applicants WHERE second_mail = %s", (email,))
            if cursor.fetchone()[0] == 0:
                emails.append(email)
                break
            counter += 1

        # Update the row
        cursor.execute("UPDATE applicants SET second_mail = %s WHERE id = %s", (email, id))
        db.commit()

        # Generate the secondary password
        # Define the characters that can be used in the password
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_characters = string.punctuation

        # Ensure the password includes at least one lowercase letter, one uppercase letter, one digit, and one special character
        password = [
            random.choice(lowercase_letters),
            random.choice(uppercase_letters),
            random.choice(digits),
            random.choice(special_characters)
        ]

        # Fill the rest of the password with random choices from all characters
        for _ in range(16 - len(password)):
            password.append(random.choice(lowercase_letters + uppercase_letters + digits + special_characters))

        # Shuffle the characters to ensure randomness
        random.shuffle(password)

        # Join the characters to get the final password
        sec_password = ''.join(password)

        # Update the row
        cursor.execute("UPDATE applicants SET sec_password = %s WHERE id = %s", (sec_password, id))
        

    db.commit()
    cursor.close()
    db.close()

    time.sleep(1)

    # Now iterate over the emails list in the second loop
    for email in emails:
        print(email)
        db = mysql.connector.connect(
            host="eivor.aserv.co.za",
            user="bluenskg_info",
            password="mmDev2024%%",
            database="bluenskg_student_space"
        )

        cursor = db.cursor()

        create_email_btn = driver.find_element(By.ID, "btnCreateEmailAccount")
        create_email_btn.click()

        time.sleep(3)
        # Split the email at the '@' character and take the first part
        email_prefix = email.split('@')[0]


        # Fetch the secondary password from the database
        cursor.execute("SELECT sec_password FROM applicants WHERE second_mail = %s", (email,))
        sec_password = cursor.fetchone()[0]

        email_input = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "txtUserName")))
        email_input.clear()
        email_input.send_keys(email_prefix)


        password_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "txtEmailPassword")))
        password_input.clear()
        password_input.send_keys(sec_password)

        # Scroll down all the way before the create button is clicked
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(1)
        
        create_btn = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "btnCreateEmailAccount")))
        create_btn.click()

        # Wait for the email account to be created
        time.sleep(2)
    
    

# Set the correct path to the Edge WebDriver
edge_driver_path = r"C:/Selenium_Driver/msedgedriver.exe"
os.environ['PATH'] += os.pathsep + edge_driver_path

# Create a WebDriver instance for Microsoft Edge
options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)  # Keep the browser open

driver = webdriver.Edge(options=options)

# Set the window size to 1024x768 (or any size where the element is visible)
driver.set_window_size(1024, 768)

# Open the website
driver.get("https://cpanel.bluenroll.co.za")

time.sleep(10)

username = driver.find_element(By.ID, "user")
username.send_keys("bluenskg")

password = driver.find_element(By.ID, "pass")
password.send_keys("mmDev2024%%")

login_btn = driver.find_element(By.ID, "login_submit")
login_btn.click()

time.sleep(7)

email_section = driver.find_element(By.ID, 'item_email_accounts')
email_section.click()

time.sleep(3)

create_email_btn = driver.find_element(By.ID, "btnCreateEmailAccount")
create_email_btn.click()

time.sleep(3)

second_mail_creation_procedure()

# Keep the browser open (optional)
input("Press Enter to close the browser...")  # Wait for user input
driver.quit()  # Close the browser when the user presses Enter        


