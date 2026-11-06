# 全台首購｜成交、房貸與現金流

可直接部署到 Streamlit Community Cloud 的完整單檔 Python 專案。預設臺北市北投區；左側可選全台22縣市、368個鄉鎮市區，也可選高雄市鼓山區。房貸與現金流不需先匯入成交資料。

## 更新既有網站

1. 使用本包新版 app.py 覆蓋 GitHub 儲存庫根目錄的同名檔案。
2. requirements.txt 套件沒有新增；若原儲存庫缺少它，請一併上傳。
3. 按 Commit changes，等 Streamlit 自動重新部署，重新開啟網站。
4. 左側預設臺北市／北投區；改選高雄市後，行政區預設鼓山區，亦可選其他行政區。
5. 個人暫存模式會自動取得所選縣市資料。已載入同縣市後切換行政區，直接使用同一縣市資料篩選；切換到其他縣市時會取得對應主檔，切回已載入縣市不重複下載。

初次部署：登入 https://share.streamlit.io ，Create app → 選GitHub儲存庫與main分支 → Main file path為app.py → Advanced settings選Python 3.11 → Deploy。基本模式Secrets留空，不需要OpenAI key。可設定可用的streamlit.app子網域，但免費服務不保證永久可用或永不休眠，詳見 https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app 。本次未登入使用者帳號完成線上部署。

## 使用方式

- 資料匯入與品質：自動載入近期可取得的最多2季，最多檢查3季；官方公開資料快取6小時。顯示所選行政區的原始版本數、合格數與排除原因。
- 自動下載失敗可按「重新取得官方資料」，或從 https://plvr.land.moi.gov.tw/DownloadOpenData 依官方流程手動下載後上傳。失敗不代表零成交，不繞過存取限制。
- 手動ZIP可含全台檔案，程式只讀目前所選縣市買賣主檔。CSV必須是該縣市官方原檔，例如臺北市a_lvr_land_a.csv、高雄市e_lvr_land_a.csv，勿將檔案改名混用。
- 成交查詢只顯示所選縣市與行政區的合格交易，可依路段篩選及匯出CSV。
- 可比估值只使用同縣市、同行政區、同路段及型態案例。路段可手動輸入；頁面列出已載入路段，建物型態下拉選單來自該地區資料。少於5筆不產生區間。
- 房貸與現金流：預設可動用現金500萬、月實領12萬，均可修改。利率及費用是情境，不是銀行報價。修改表單後按計算更新，可下載逐月攤還及試算JSON。詳見FINANCE.md。

## 資料保存與外接資料庫

預設每位訪客使用獨立記憶體SQLite；切換地區不清除已載入縣市，重新連線或重啟仍可能清空。個人試算不寫入成交資料庫。

可在data/放置官方縣市CSV快照，例如data/a_lvr_land_a.csv、data/e_lvr_land_a.csv；首次選該縣市時匯入。請保留來源網址、季別、下載日期與SHA256憑證。快照不自動更新，且上傳GitHub後會公開。預設.gitignore忽略data，若用Git命令上傳，需自行明確加入公開檔案。

如需共用保存，可在Cloud的Secrets設定DATABASE_URL與IMPORT_PASSWORD（勿上傳真密碼到GitHub）：

~~~toml
DATABASE_URL = "postgresql+psycopg://USER:URL_ENCODED_PASSWORD@HOST:5432/DBNAME?sslmode=require"
IMPORT_PASSWORD = "自行設定的長管理密碼"
~~~

外接共用資料庫時不由訪客自動寫入，須輸入管理密碼才能手動下載/匯入；未設密碼時匯入關閉。查詢仍公開，只存可公開資料。資料庫供應商的免費額度、休眠與備份另計，本機SQLite檔在Cloud不保證持久。AUTO_LOAD = "false"可關閉自動取得。

**舊資料庫升級：**全台版新增city欄位，使用transactions_v2與imports_v2新表，不刪除或改寫舊版transactions/imports。舊版資料不會自動遷移，需重新匯入官方檔案，避免跨縣市混淆。v2原始列雜湊包含縣市；同縣市原始列重複匯入不增加筆數。

## 資料來源與模型

行政區離線清單擷取自國土測繪中心官方 https://api.nlsc.gov.tw/other/ListCounty 與 https://api.nlsc.gov.tw/other/ListTown1/{countycode} ，2026-11-06查核，共22縣市368區。縣市字母代碼與官方114S4 ZIP全部22個買賣主檔核對。行政區如日後調整須更新清單。

成交資料出處：內政部地政司。依官方使用規範取得並註明出處；本工具非官方認可鑑價服務。各縣市檔會清洗並保存所有行政區，頁面再按所選行政區篩選；不能把縣市匯入總筆數當成單一行政區成交數。

詳細估值規則、缺失與限制見MODEL_NOTES.md；房貸假設見FINANCE.md；實測範圍見VALIDATION.md。

## 本機啟動

~~~powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
~~~

單檔版不需要beitou模組資料夾。另提供模組化原始專案與完整測試，給需要開發或CLI批次匯入者。
