## 自動取得版更新

上傳新版 app.py 後，個人暫存模式首次開啟會自動取得官方季度成交資料，不必先下載或上傳。依台灣日期從最近完整季度往前最多檢查3季，載入最多2個可用季度。只共用官方公開資料的6小時快取，每個訪客資料庫仍獨立。右側顯示來源、季別、雜湊與排除統計；左側「重新取得官方資料」可清除快取並重試。下載失敗不代表沒有成交，仍保留手動匯入。此功能不保證完整兩年，也不是背景排程或即時更新。

若已有隨儲存庫快照，先使用快照；需要新資料時按重新取得。外接共用資料庫時不由訪客自動寫入，維持管理者匯入模式。可在 Secrets 設定 AUTO_LOAD = "false" 關閉自動取得。

# 免費部署到 Streamlit Community Cloud

這份專案包含完整 Python 程式碼，預設不需要 OpenAI API key、信用卡、Docker 或外部資料庫。下載 ZIP 並解壓縮後，請把**資料夾裡的檔案**上傳 GitHub 儲存庫根目錄。

## 先理解網址與儲存

部署後可得到固定的 `https://你的子網域.streamlit.app` 網址。**免費服務沒有「永久有效、永不休眠」的保證**：官方目前規定閒置 12 小時會休眠，訪客可點選喚醒；平台規範、帳號、儲存庫或應用刪除等仍會影響可用性。請勿把未部署的範例網址當成真實網站。

官方說明：[部署與網址](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy)、[休眠規則](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app)、[本機儲存不保證持久](https://docs.streamlit.io/develop/concepts/connections/connecting-to-data)。查核日：2026-11-06。

預設使用每個訪客獨立的記憶體 SQLite；上傳/下載匯入的資料只在該連線暫存，重新整理、斷線或重啟後可能需要重新匯入。其他訪客不能修改你的暫存資料。這不會讓資料隨網址永久保存。

## 1. 建立 GitHub 儲存庫

1. 登入 [GitHub](https://github.com)，選擇 New repository。
2. 名稱例如 `beitou-homevalue`，選擇 Public，建立儲存庫。
3. 點 Add file → Upload files，將解壓縮專案內的檔案與資料夾一起上傳。不要只上傳 ZIP，也此單檔版本不需要 beitou 資料夾。
4. Commit changes。至少要有 `app.py`、`requirements.txt`；建議整包上傳。`.streamlit/config.toml` 是選用外觀/上傳容量設定。某些系統隱藏點開頭資料夾，可手動在 GitHub 建立該路徑。

## 2. 建立雲端應用

1. 開啟 [Streamlit Community Cloud](https://share.streamlit.io)，以 GitHub 帳號登入並完成網站要求的授權。
2. 點 Create app／Deploy an app，選擇剛才的 Repository。
3. Branch 選 `main`，Main file path 填 `app.py`（若你把整個資料夾上傳成子目錄，則需填實際路徑，建議直接放根目錄）。
4. App URL / Custom subdomain 可輸入 `beitou-homevalue-你的英文代號`；若名稱已被使用，換一個。
5. Advanced settings 選擇 Python 3.11。基本模式 Secrets 留空。
6. 點 Deploy，等套件安裝與啟動。成功後複製真正產生的 `streamlit.app` 網址分享。

目前套件使用相容版本範圍；本次本機測試環境為 Python 3.9 / Streamlit 1.50，未登入你的帳號完成 Cloud 實測。Python 3.11 是此專案的建議雲端版本。部署失敗請先查看 Cloud logs，不要將密碼貼到公開 issue。

## 3. 匯入與估值

在「資料匯入與品質」輸入民國季別，例如 `114S4`，點「下載並匯入指定季別」。如果內政部網站拒絕雲端下載，請依[官方網頁](https://plvr.land.moi.gov.tw/DownloadOpenData)流程手動下載 ZIP，再上傳。也可上傳官方臺北市買賣主檔 `a_lvr_land_a.csv`。

資料清洗後可進入成交查詢與可比估值。只有足夠的同類型實際成交才輸出區間，不將刊登開價當成成交價。詳細清洗、車位分拆及估值限制請讀 MODEL_NOTES.md。

## 可選：讓每次開啟都有固定成交資料

將官方臺北市買賣 CSV 以 `data/a_lvr_land_a.csv` 上傳 GitHub。未外接資料庫時，每個新連線會自動匯入這份快照，不需訪客重新下載。

- 只放依法可公開的官方檔案，不要上傳個人提供的敏感資料。
- 保留官方下載網址、季別、下載日期及 SHA256 來源憑證，例如 `data/source.json`。這些檔案會隨儲存庫公開。
- 預設 .gitignore 忽略 data 資料；若用 Git 命令上傳，需明確執行 `git add -f data/a_lvr_land_a.csv data/source.json`，或使用 GitHub 網頁上傳。
- 單季資料可能不足五筆可比，應逐季建立涵蓋期更完整的外接資料庫。檔案與大量訪客匯入會消耗免費主機資源；快照適合小型展示。
- 版本庫裡的快照是固定版本，不會自動更新為最新實價。

## 可選：外接 PostgreSQL 保存共用資料

自行取得可連線的 PostgreSQL 服務，在 Cloud 的 Advanced settings / Secrets 貼入：

```toml
DATABASE_URL = "postgresql+psycopg://USER:URL_ENCODED_PASSWORD@HOST:5432/DBNAME?sslmode=require"
IMPORT_PASSWORD = "請換成自己設定的長管理密碼"
```

這些是格式範例，需替換為真正的連線資訊；密碼的特殊字元需 URL 編碼。不要把 Secrets 寫進公開 GitHub。外接資料庫自己的免費額度、休眠、備份與保留政策另計，亦無永久免費保證。

設定 DATABASE_URL 後資料由訪客共用。只有輸入正確管理密碼才能透過頁面匯入；未設管理密碼時，頁面匯入會關閉。頁面查詢仍是公開的，只應存放可公開成交資料。此密碼閘門是小型展示用途，並非完整多人權限或稽核系統。若把 DATABASE_URL 設成雲端本機 SQLite 檔，仍不保證資料保存。

官方 [Secrets 操作說明](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)。

## 本機啟動

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

雲端單檔版包含完整 ETL、資料儲存、估值與頁面函式；原始模組專案另附完整測試。
