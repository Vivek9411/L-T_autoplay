from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from pathlib import Path
import time

chromedriver_path = "chromedriver-win64/chromedriver.exe"  # Replace with the actual path to your chromedriver

# For Windows, use: "chromedriver-windows/chromedriver.exe"
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
# optional: use your real user-agent
options.add_argument("user-agent=gopal")
# Initialize undetected Chrome driver
driver = uc.Chrome(driver_executable_path=str(chromedriver_path))



# driver.get("https://bot.sannysoft.com/")
# time.sleep(15)
# driver_path = "chromedriver-linux64/chromedriver"  # Replace with the actual path to your chromedriver
# service = Service(driver_path)
#
# # Initialize the WebDriver with the Service
# driver = webdriver.Chrome(service=service)
# course = 0


# optional: use your real user-agent
# options.add_argument("user-agent=YourCustomUserAgentHere")

url = 'https://ietllearnkonnect.lntedutech.com/Home'
driver.get(url)
time.sleep(5)

# email = ""  # add your email
# password = '' # add your password
# password = 'xIiYnRJ@123'
# time.sleep(5)
driver.find_element(By.XPATH, '/html/body/app-root/div/app-header/header/div/div[3]/div[2]/button').click()
time.sleep(5)
driver.find_element(By.ID, 'email').send_keys(email)
time.sleep(2)
driver.find_element(By.ID, 'Password').send_keys(password)
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, 'app-login .ng-star-inserted button').click()
time.sleep(10)


# driver.find_element(By.CSS_SELECTOR, '.myLearning').click()
# time.sleep(20)
# skip_courses = [7,15]
# all_courses = driver.find_elements(By.CSS_SELECTOR, '.coursesLearning .dragScrollItem .card .cardImg')
# print(len(all_courses))
#
# for idx, course in enumerate(all_courses):
#     if id not in skip_courses:
#         print(course.text, 'text')
# print('done')

time.sleep(50)


# all_scroll_buttons = driver.find_elements(By.CSS_SELECTOR, '.arrowExpandCollapse')
all_scroll_button= WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '.arrowExpandCollapse')))
all_scroll_buttons = driver.find_elements(By.CSS_SELECTOR, '.arrowExpandCollapse')
print(len(all_scroll_buttons))


played_video = []
def play_video(driver, title,outer_iframe_id='myPlayer', inner_iframe_id='content', video_id='video'):
    try:
        print("Trying to play video...")

        # 1. Switch to outer iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, outer_iframe_id))
        )
        print(f"Switched to outer iframe: {outer_iframe_id}")

        # 2. Switch to inner iframe
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, inner_iframe_id))
        )
        print(f"Switched to inner iframe: {inner_iframe_id}")

        # 3. Wait for video element
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, video_id))
        )
        print("Video element found.")

        # 4. Try to get video duration
        duration = None
        for _ in range(10):  # Retry until duration is available
            duration = driver.execute_script(f"""
                const video = document.getElementById('{video_id}');
                return video && video.readyState >= 1 ? video.duration : null;
            """)
            if duration:
                break
            print("Waiting for video metadata...")
            time.sleep(5)

        if duration:
            print(f"Video duration: {duration:.2f} seconds")

            # 5. Simulate user interaction by clicking the video
            video_element = driver.find_element(By.ID, video_id)
            video_element.click()
            time.sleep(1)

            # 6. Mute and play the video using JS
            driver.execute_script(f"""
                const video = document.getElementById('{video_id}');
                if (video) {{
                    video.muted = true;
                    video.play();
                    console.log("Video is playing");
                    
                }}
            """)
            print("Playback started.")
            played_video.append(title)
        else:
            print("Failed to retrieve video duration.")

        # 7. Switch back to main page
        driver.switch_to.default_content()

        return duration

    except Exception as e:
        print("Error during playback:", e)
        driver.switch_to.default_content()
        return None

time.sleep(20)
temp = 0


while True:
    lets_break = False

    if temp==0:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.arrowExpandCollapse .expand_more'))
        )
        buttons = driver.find_elements(By.CSS_SELECTOR, '.arrowExpandCollapse .expand_more')
        for button in buttons:
            button.click()
            time.sleep(2)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li .icov'))
    )
    all_videos = driver.find_elements(By.CSS_SELECTOR, 'ul li .icov')
    # temp=len(all_videos)
    for idx, video in enumerate(all_videos):
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'ul li h3'))
            )
            print(video.find_element(By.CSS_SELECTOR, 'h3').text)
            title = video.find_element(By.CSS_SELECTOR, 'h3').text
            if video.find_element(By.CSS_SELECTOR, 'h3').text=='Final Assessment':
                print('Time to gooo bbyeee, task completed')
                lets_break=True
                break
            # print(video.find_element(By.CSS_SELECTOR, 'span').text)
            # print(video.find_element(By.CSS_SELECTOR, 'span').get_attribute('class'))
            try:
                class_atrrib = video.find_element(By.CSS_SELECTOR, 'span').get_attribute('class')
                print(class_atrrib)
            except Exception as e:
                print('inner error class_atrib not found')
                class_atrrib=None
            if (not class_atrrib or 'bgGreen' not in class_atrrib) and (title not in played_video):
                try:
                    video.click()
                    time_of_video = play_video(driver=driver, title=title)
                    time.sleep(time_of_video+30)
                    if temp==0:
                        temp = 2
                        break
                    else:
                        time.sleep(20)
                    temp = 2
                except Exception as e:
                    print('cannot click video')
        except Exception as e:
            print('video not found to click')
            break

    print('loop completes ', temp)
    temp-=1
    if lets_break:
        break
    driver.refresh()
    time.sleep(15)
