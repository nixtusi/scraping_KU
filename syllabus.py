from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# 曜日マップ（1:月, 2:火, ..., 5:金）
yobi_map = {
    "1": "月",
    "2": "火",
    "3": "水",
    "4": "木",
    "5": "金"
}

# Chrome 起動
print("🧭 Chromeドライバ起動中...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://kym22-web.ofc.kobe-u.ac.jp/campussy/campussquare.do?_flowExecutionKey=_c9FD8A8D3-2BF5-D0BA-A2B5-94B5ACABB3C4_kCA785021-D4A5-A09B-FEED-F1FCE48160EA")

print("🌐 シラバスページにアクセス完了")

# 工学部を表示（JS実行）
try:
    WebDriverWait(driver, 10).until(
        #EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, \"SelectSearchCall('2025/09')\")]"))
        EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, \"SelectSearchCall('2025/05')\")]"))
    )
    #driver.execute_script("SelectSearchCall('2025/09')")
    driver.execute_script("SelectSearchCall('2025/05')")
    print("✅ 工学部の講義一覧を表示")
except Exception as e:
    print("❌ 工学部選択失敗:", e)
    driver.quit()
    exit()

# 各曜日でループ
for yobi_code in ["1", "2", "3", "4", "5"]:
    try:
        print(f"🔁 {yobi_map[yobi_code]}曜日を選択中...")
        time.sleep(1)  # JS反映待機
        driver.execute_script(f"SelectYobiCall('{yobi_code}')")
        time.sleep(1.5)  # 表示切り替え待機

        # BeautifulSoupで講義表を取得
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", class_="normal")

        if not table:
            print(f"❌ {yobi_map[yobi_code]}曜日のテーブルが見つかりません")
            continue

        rows = table.find_all("tr")[1:]  # ヘッダー除外
        print(f"📚 {yobi_map[yobi_code]}曜日の講義数: {len(rows)}")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 8:
                course = {
                    "科目名": cols[4].text.strip(),
                    "担当": cols[5].text.strip(),
                    "曜日・時限": cols[6].text.strip(),
                    "コード": cols[7].text.strip()
                }
                print(f"・{course['科目名']} / {course['担当']} / {course['曜日・時限']} / {course['コード']}")

    except Exception as e:
        print(f"❌ {yobi_map[yobi_code]}曜日処理中にエラー:", e)

print("🛑 処理完了、Chromeを閉じます")
driver.quit()