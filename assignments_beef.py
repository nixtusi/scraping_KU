from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs4
import time

print("🧭 Chromeドライバ起動中...")
try:
    driver = webdriver.Chrome()
except Exception as e:
    print("⚠️ ローカルにChromeDriverが見つからなかったため、インストールして起動します")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

bace_url = "https://beefplus.center.kobe-u.ac.jp"
login_url = "/saml/loginyu?disco=true"
target_url = "/lms/task"

number = "24XXXXXt" # 学生番号（例: XXXXXXXx）
password = "PPPPPPPPP" # パスワード（例: XXXXXXXX）

print("🌐 ログインページにアクセス中...")
driver.get(bace_url + login_url)
time.sleep(0.5)

try:
    print("🔐 ログイン情報を入力中...")
    in_num = driver.find_element(By.ID, "username")
    in_pass = driver.find_element(By.ID, "password")
    button = driver.find_element(By.ID, "kc-login")

    in_num.send_keys(number)
    in_pass.send_keys(password)
    button.click()
    print("✅ ログインボタンをクリックしました")
except Exception as e:
    print("❌ ログイン処理に失敗しました:", e)
    driver.quit()
    exit()

time.sleep(0.5)

print("📄 タスクページに遷移中...")
driver.get(bace_url + target_url)
time.sleep(0.5)

html = driver.page_source
soup = bs4(html, "html.parser")

print("🔍 タスク情報を取得中...")
courses = soup.find_all("div", class_="course")
deadlines = soup.find_all("span", class_="deadline")

if not courses or not deadlines:
    print("⚠️ タスクや締切が見つかりませんでした")
else:
    print(f"📚 {len(courses)} 件のタスクが見つかりました：")
    for c, d in zip(courses, deadlines):
        deadline = d.get_text(strip=True)
        course = c.get_text(strip=True)
        print(f"📝 [{course}] の締切：{deadline}")

print("🛑 処理完了、Chromeを閉じます")
driver.quit()