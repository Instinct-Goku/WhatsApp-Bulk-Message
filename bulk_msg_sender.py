from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from message import msg

# Function to simulate "Shift + Enter" for line breaks
def send_multiline_message(message_box, message):
    lines = message.split('\n')  # Split message by lines
    for i, line in enumerate(lines):
        message_box.send_keys(line)  # Send the current line
        if i < len(lines) - 1:  # If it's not the last line
            message_box.send_keys(Keys.SHIFT + Keys.RETURN)  # Simulate Shift+Enter for a new line
        time.sleep(0.5)  # Short delay between sending lines

def send_images(phone_number,images,driver):
    time.sleep(15)  # Wait for the page to load the chat
     #send image
    try:
        for image_path in images:
            attach_button = driver.find_element(By.CSS_SELECTOR, 'span[data-icon="plus"]')
            attach_button.click()
            time.sleep(1)
            image_input = driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
            image_input.send_keys(image_path)
            time.sleep(5)

            # Click send button
            send_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_button.click()
            time.sleep(5)
    except Exception as e:
        print(f"Failed to send to {phone_number}: {e}")

        time.sleep(2)

def send_msg(driver):
     #send message
    message = msg
    # message.format() Format the message 
    try:
        message_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        send_multiline_message(message_box, message)  # Send the multi-line message
        message_box.send_keys(Keys.RETURN)  # Press Enter to send the message
        time.sleep(2)
        print(f'Message sent to {phone_number}')
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
    
# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

# wait for wp to load and press enter
input("Please scan the QR code to log in.")


# Read the CSV file containing phone numbers and messages
with open(file='./wadala-boys.csv', mode='r') as file:
    reader = csv.DictReader(file)
    img_path_list = "D:\hack-scripts\Whatsapp-scripts\wadala.jpeg"

    for row in reader:
        phone_number = row['mobile']
        name = row['name']
        # message = "Hare Krishna!! " + "**" + name + "**"+ "\n\nyou're invited for SATURDAY YOUTH PROGRAM AT WADALA\nPLZ CHECK THE DETAILS\n**5:45 PM to 7 PM**\n**7 PM - 8:15 PM** Kirtan Arti & Meditation\nDinner Prasadam at the end\nVENUE: ISKCON Wadala outpost, Flat no 8, Shankar Dham, Opposite Allahabad Indian Bank, Near SIWS COLLEGE, Wadala west, Mumbai.\n\nReply if you or anyone from your contacts, friends , family can join In Wadala area."

        if phone_number == '':
            print('Empty mobile number for ' + row['Name'])
            continue

        # Ensure that each phone number is properly formatted
        for number in phone_number.split(','):
            phone_number_url = f"https://web.whatsapp.com/send?phone={phone_number}"
            driver.get(phone_number_url)
            # send image list
            send_images(number, img_path_list.split(','), driver)
            send_msg(driver)

            time.sleep(5)  # Wait before sending the next message

# Close the browser
driver.quit()
