import warnings
warnings.filterwarnings("ignore", message=".*NotOpenSSLWarning.*")

import time
import random
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mail import send_email
from datetime import datetime, timedelta
import os

try:
    # date
    days_ahead = int(os.getenv("DAYS_AHEAD"))
    def parse_date(date_str):
        parts = date_str.strip().split(" ")
        date_part = parts[-1]
        
        nums = date_part.split(".")
        day = int(nums[0])
        month = int(nums[1])
        year = int(nums[2]) if len(nums) > 2 else datetime.today().year
        return datetime(year, month, day)

    # exam type
    exam_type = os.getenv("EXAM_TYPE")
    FILES = {
        "praktyka": {
            "dates": "dates-practice.txt",
            "new": "new-practice.txt"
        },
        "teoria": {
            "dates": "dates-theoretical.txt",
            "new": "new-theoretical.txt"
        }
    }

    while True:
        now = datetime.now()
        is_sunday = (now.weekday() == 6)
        is_work_hours = (7 <= now.hour < 16)

        if is_sunday or not is_work_hours:
            candidate = now.replace(hour=7, minute=0, second=0, microsecond=0)
            if now >= candidate:
                candidate += timedelta(days=1)
            while candidate.weekday() == 6:
                candidate += timedelta(days=1)

            secs = (candidate - now).total_seconds()
            h, m = int(secs) // 3600, (int(secs) % 3600) // 60
            print(f"[{now}] poza godzinami pracy (7-16) lub niedziela")
            print(f"Następna próba o {candidate.strftime('%Y-%m-%d 07:00')} (za {h}h {m}min)")
            time.sleep(secs)
            continue

        cutoff_date = datetime.today() + timedelta(days=days_ahead)
        print("")    
        print("Rozpoczęto sesje pobierania danych")
        print(f"Data do której szuka terminów: {cutoff_date}")

        def human_delay(min_s=0.5, max_s=1.5):
            time.sleep(random.uniform(min_s, max_s))

        print(f"Uruchamianie chromium")
        driver = uc.Chrome(headless=False)
        wait = WebDriverWait(driver, 60)
        print("Chromium uruchomione")

        human_delay()
        print("Nawigowanie do strony logowania")
        driver.get("https://info-car.pl/oauth2/login")

        print("Wpisywanie logina i hasła")
        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(os.getenv("LOGIN"))
        human_delay()
        driver.find_element(By.ID, "password").send_keys(os.getenv("LOGIN_PASSWORD"))
        human_delay()
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait.until(EC.url_contains("/new"))
        print("Zalogowano pomyślnie")
        human_delay()

        driver.get("https://info-car.pl/new/prawo-jazdy/sprawdz-wolny-termin")
        human_delay()

        # cookies
        try:
            accept = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cookiescript_accept")))
            accept.click()
            human_delay()
        except:
            try:
                driver.execute_script("""document.querySelectorAll('[id^="cookiescript"] button, #cookiescript_accept').forEach(btn => btn.click());""")
            except:
                pass

        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cookiescript_checkbox_label")))
        except:
            pass

        # pkk
        print("Wybieranie pkk")
        pkk = wait.until(EC.presence_of_element_located((By.ID, "exam")))
        driver.execute_script("arguments[0].scrollIntoView(true);", pkk)
        human_delay()
        driver.execute_script("arguments[0].click();", pkk)
        human_delay()

        # province
        province_env = os.getenv("PROVINCE")
        print(f"Wybieranie województwa: {province_env}")
        province_input = wait.until(EC.presence_of_element_located((By.ID, "province")))
        try:
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
        except:
            pass
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", province_input)
        human_delay()
        driver.execute_script("arguments[0].click();", province_input)

        province_selected = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space(text())='{province_env}']")))
        human_delay()
        driver.execute_script("arguments[0].click();", province_selected)
        human_delay()

        # center
        center_env = os.getenv("CENTER")
        print(f"Wybieranie ośrodka WORD: {center_env}")
        wait.until(lambda d: d.find_element(By.ID, "organization").is_enabled())
        center_input = driver.find_element(By.ID, "organization")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", center_input)
        human_delay()
        driver.execute_script("arguments[0].click();", center_input)

        center_selected = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[contains(text(), '{center_env}')]")))
        human_delay()
        driver.execute_script("arguments[0].click();", center_selected)
        human_delay()

        # category
        category_env = os.getenv("CATEGORY")
        print(f"Wybieranie kategorii: {category_env}")
        category = wait.until(EC.presence_of_element_located((By.ID, "category-select")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", category)
        human_delay()
        driver.execute_script("arguments[0].click();", category)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "si-internal-result-list .results")))

        categorySelected = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[normalize-space(text())='{category_env}']")))
        human_delay()
        driver.execute_script("arguments[0].click();", categorySelected)
        human_delay()

        print("Klikanie przycisk \"Dalej\"")
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cdk-overlay-backdrop")))
        btn_next = wait.until(EC.presence_of_element_located((By.XPATH, "//button[.//span[text()='Dalej']]")))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn_next)
        human_delay()
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(driver).move_to_element(btn_next).click().perform()

        # exam type
        exam_type_env = os.getenv("EXAM_TYPE")
        print(f"Wybieranie typ egzaminu: {exam_type_env}")
        if (exam_type_env == "praktyka"):
            exam_type_input = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='practical-container']/input")))
        elif (exam_type_env == "teoria"):
            exam_type_input = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='theoretical-container']/input")))
        driver.execute_script("arguments[0].scrollIntoView(true);", exam_type_input)
        human_delay()
        driver.execute_script("arguments[0].click();", exam_type_input)
        human_delay()

        # dates
        print("Pobieranie danych")

        no_exams = driver.find_elements(By.CSS_SELECTOR, "#no-exams-label > span")
        if no_exams and "Brak egzaminów spełniających wybrane kryteria" in no_exams[0].text:
            print("Brak egzaminów spełniających wybrane kryteria")
            driver.quit()
            raise SystemExit

        try:
            accordion_items = driver.find_elements(By.CSS_SELECTOR, "div.accordion-item")
            current_entries = []

            for item in accordion_items:
                try:
                    header_btn = item.find_element(By.CSS_SELECTOR, "button.accordion-button")
                except:
                    continue

                try:
                    expanded = header_btn.get_attribute("aria-expanded")
                    if expanded != "true":
                        driver.execute_script("arguments[0].click();", header_btn)
                        human_delay()
                except:
                    pass

                try:
                    date_text = item.find_element(By.CSS_SELECTOR, "h5.m-0").text.strip()
                except:
                    continue

                try:
                    slot_date = parse_date(date_text)
                    if slot_date > cutoff_date:
                        continue
                except Exception as e:
                    continue

                rows = item.find_elements(By.CSS_SELECTOR, "div.theory-row")

                for row in rows:
                    try:
                        time_text = row.find_element(By.CSS_SELECTOR, "p.exam-time span").text.strip()
                    except:
                        continue

                    try:
                        info_text = row.find_element(By.CSS_SELECTOR, "p.additional-info").text.strip()
                    except:
                        info_text = ""

                    info_text = " ".join(info_text.split())

                    current_entries.append(f"{date_text} | {time_text} | {info_text}")
            print(f"Nowych terminów: {len(current_entries)}")

            old_entries = []
            try:
                with open(FILES[exam_type]["dates"], "r", encoding="utf-8") as f:
                    old_entries = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                pass

            new_entries = [e for e in current_entries if e not in old_entries]
            if new_entries:
                print("====================")
                print(f"!!! NOWE TERMINY ZNALEZIONO ({len(new_entries)}) !!!")
                print("====================")

                send_email(
                    subject=f'NOWE TERMINY "{os.getenv("EXAM_TYPE")}" INFO-CAR!!!',
                    body="\n".join(new_entries)
                )

                with open(FILES[exam_type]["new"], "w", encoding="utf-8") as f:
                    f.write("\n".join(new_entries))
            else:
                print("====================")
                print("brak nowych terminów")
                print("====================")

                with open(FILES[exam_type]["new"], "w", encoding="utf-8") as f:
                    pass

            with open(FILES[exam_type]["dates"], "w", encoding="utf-8") as f:
                f.write("\n".join(current_entries))

        finally:
            print("Zamykanie sesji")
            driver.quit()

        min_frequency_env = int(os.getenv("MIN_FREQUENCY"))
        print(f"Czekanie {min_frequency_env}min na następną sesję")
        time.sleep(min_frequency_env * 60)
except KeyboardInterrupt:
    print("")
    print("Zamknięto bota: infocar-scraper")