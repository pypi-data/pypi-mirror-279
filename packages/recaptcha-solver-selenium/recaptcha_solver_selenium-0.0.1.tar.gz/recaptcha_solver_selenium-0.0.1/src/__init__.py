from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import requests
import logging
import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver


def solve_captcha(driver: webdriver, iframe, timeout=15, click_box=True):
    """
    Solves the reCAPTCHA challenge on a webpage using audio recognition.

    Args:
        - driver (webdriver): Selenium WebDriver instance.
        - iframe (WebElement): The iframe containing the reCAPTCHA challenge.
        - timeout (int): Maximum time to wait for elements to appear.

    Raises:
        - Exception: If unable to find necessary elements or download audio.

    """
    tmp_files = [os.path.join(tempfile.gettempdir(), "_tmp.mp3"),
                 os.path.join(tempfile.gettempdir(), "_tmp.wav")]
    wait = WebDriverWait(driver, timeout)

    try:
        # Switch to the reCAPTCHA iframe
        driver.switch_to.frame(iframe)

        # Click the checkbox to start the challenge
        if click_box:
            wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'recaptcha-checkbox-border'))
            ).click()

        # Switch back to the main frame
        driver.switch_to.default_content()

        # Switch to the audio challenge iframe
        driver.switch_to.frame(
            wait.until(
                EC.visibility_of_element_located((By.XPATH, "//iframe[contains(@title, 'recaptcha')]"))
            )
        )

        # Click the audio challenge button to get the audio challenge
        wait.until(
            EC.element_to_be_clickable((By.ID, "recaptcha-audio-button"))
        ).click()

        # Download the audio challenge file
        download_link = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "rc-audiochallenge-tdownload-link"))
        ).get_attribute("href")

        if not download_link:
            raise Exception('Failed to find audio download link')

        # Save the audio file locally
        with open(tmp_files[0], "wb") as f:
            r = requests.get(download_link, allow_redirects=True)
            f.write(r.content)

        # Convert audio from MP3 to WAV format
        AudioSegment.from_mp3(tmp_files[0]).export(tmp_files[1], format="wav")

        # Perform audio recognition using Google's speech recognition API
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_files[1]) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Input the recognized text into the reCAPTCHA input field
        wait.until(
            EC.presence_of_element_located((By.ID, "audio-response"))
        ).send_keys(text)

        # Click the "Verify" button to complete reCAPTCHA solving
        wait.until(
            EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
        ).click()

    except Exception as e:
        logging.error(f"Error solving reCAPTCHA: {e}")

    finally:
        __cleanup(tmp_files)


def __cleanup(files: list):
    """
    Cleans up temporary files created during the solving process.

    Args:
        - files (list): List of file paths to be deleted.

    """
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)
