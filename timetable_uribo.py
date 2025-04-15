from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

number = "2435109t"
password = "SdjTf=8Q"
quarter = 2

print("🧭 Chromeドライバ起動中...")
try:
    driver = webdriver.Chrome()
except:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

print("🌐 ログインページにアクセス中...")
driver.get("https://kym22-web.ofc.kobe-u.ac.jp/campusweb")

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(number)
driver.find_element(By.ID, "password").send_keys(password)
driver.find_element(By.ID, "kc-login").click()
print("✅ ログイン完了！")

# アンケートボタン
try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "HissuKaitoInputForm-auto-input-3"))).click()
    print("✅ アンケートボタンをクリックしました")
except:
    print("ℹ️ アンケートボタンは表示されていません（スキップ）")

# 「履修・抽選」→「履修登録・登録状況照会」
try:
    menu1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "履修・抽選")))
    driver.execute_script("arguments[0].click();", menu1)
    print("📂 『履修・抽選』をクリック（JS実行）")

    menu2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "履修登録・登録状況照会")))
    driver.execute_script("arguments[0].click();", menu2)
    print("📂 『履修登録・登録状況照会』をクリック（JS実行）")
except Exception as e:
    print("❌ メニュー遷移に失敗:", e)
    driver.quit()
    exit()

# 🔁 クォーターの選択
try:
    print(f"🔍 『第{quarter}クォーター』がすでに選択されているか確認中...")
    # 選択済みかどうか確認（背景画像がrs_tab_sel.gif かつ title に「表示しています」）
    selected_xpath = f"//td[contains(text(), '第{quarter}クォーター') and contains(@title, '表示しています')]"
    selected = driver.find_elements(By.XPATH, selected_xpath)

    if selected:
        print(f"✅ 『第{quarter}クォーター』はすでに選択済み")
    else:
        print(f"➡️ 『第{quarter}クォーター』を選択します...")
        link_xpath = f"//a[text()='第{quarter}クォーター']"
        quarter_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
        driver.execute_script("arguments[0].click();", quarter_link)
        print(f"📅 『第{quarter}クォーター』をクリック（JS実行）")
        time.sleep(2)
except Exception as e:
    print(f"❌ 『第{quarter}クォーター』の選択に失敗:", e)

# 時間割データ取得（講義情報）
try:
    time.sleep(1)  # JSレンダリング待機

    elements = driver.find_elements(By.CLASS_NAME, "rishu-koma-inner")
    if not elements:
        raise Exception("講義ブロックが見つかりません")

    print("🧾 時間割データ取得成功！")
    print("👇 時間割内容：")
    for elem in elements:
        try:
            text = elem.text.strip().replace("\n", "/")
            if text:
                print(f"・{text}")
        except:
            continue

except Exception as e:
    print("❌ 時間割テーブルの取得に失敗:", e)

print("🛑 処理完了、Chromeを閉じました")
driver.quit()