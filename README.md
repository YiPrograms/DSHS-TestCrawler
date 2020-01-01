# 東山數位管理系統 成績下載&整理程式

## 功能

- `crawl.py`: 

	​	從數位管理系統取得週複習考刷卡成績單

- `parse.py`: 

	​	將多個刷卡成績單合併整理成一個成績單

## 使用方法


### crawl.py

```bash
crawl.py PHPSESSID [篩選條件] [-l]
```

- PHPSESSID (PHP 會話ID):
	此為每次登入系統發派給用戶的一個隨機ID，用來辨識用戶身份
	此程式需要有權限的帳號ID才能取得成績單
	
	取得方法:
	1. 登入數位管理系統後按下 F12
	2. 選擇 主控台(Console) 頁面
	3. 執行 `document.cookie`
	4. 複製 `PHPSESSID= `之後的字串 (如: `ji8a9anc6ivljir7ag781acj22`)

- 篩選條件
	使用成績單檔名來篩選要下載的檔案
	
	檔案將會分成下列格式:
		`學年(-y)` `考試類型(-t)`成績第`週(-w)`週-`日期(-d)` (`科目(-s)`)`名稱(-n)`
		如 `108.1週考成績第10週-1003 (化學)高三-命題老師-朱威達` 將會分成:
			`[108.1]` `[週考]`成績第`[10]`週-`[1003]` (`[化學]`)`[高三-命題老師-朱威達]`
	
	篩選條件可以由許多參數組成:
	- `-y`: 學年  Ex: 108.1
	- `-t`: 考試類型 (週考/複習考/小考/暑輔 等)
	- `-w`: 週  Ex: 10
	- `-d`: 日期  Ex: 1003
	- `-s`: 科目  Ex: 化學
	- `-n`: 名稱 Ex: 高三忠孝 (只要部份包含)
	- `-nn`: 名稱不包含 Ex: 仁
	- `-c`: 自訂篩選 (篩選原始檔名) Ex: (化學)高三自然組
	
	也可以同時篩選多個條件，如:  `-w 1 2 3 -n 高一 高1`

- `-l`: 列出結果
	使用此參數將只會列出結果，不下載
	建議先加上此參數，確定結果後再下載
	
#### 範例
> 假設 PHPSESSID 為 `ji8a9anc6ivljir7ag781acj22`

- 列出所有考試:
	`crawl.py ji8a9anc6ivljir7ag781acj22 -l`

- 列出高三第10週的考試:
	`crawl.py ji8a9anc6ivljir7ag781acj22 -w 10 -n 高三 -l`

- 下載高三第10週的考試:
	`crawl.py ji8a9anc6ivljir7ag781acj22 -w 10 -n 高三`
	
- 下載高二忠孝第1,2,3週的化學考試:
	`crawl.py ji8a9anc6ivljir7ag781acj22 -w 1 2 3 -s 化學 -n 高二忠孝`

### parse.py

```bash
parse.py 班級 [--grade 年級]
```

- 班級
	由於一個成績單檔案內有多個班級，必須要指定班級才能知道要取出哪個班級
	輸入一個班級的中文代號 (`忠`/`孝`/`仁`/`愛` 等...)
	如果找不到班級，將會忽略檔案

- 年級
	輸入年級 (數字)
	非必要，可以用來確認有沒有下載錯年級的檔案
	如果年級不合，將會忽略檔案
	
#### 範例

- 整理出高三忠班的成績 (假設下載的檔案只有高三):
	`parse.py 忠`
	
- 整理出高三忠班的成績:
	`parse.py 忠 --grade 3`

## 安裝方法

- 需求:
	- Python 3
	- Libraries:
		- requests
		- argparse
		- beautifulsoup4
		- lxml
		- pandas
		- xlrd

### 正常安裝

必須要有正常的 Python 3 環境
請去 [Python官網](https://www.python.org/downloads/) 下載安裝
記得也要安裝 pip

[Windows 教學](https://pygame.hackersir.org/Lessons/01/Python_install.html) (很重要的是要勾選 `Add to PATH`)

```bash
git clone https://github.com/YiPrograms/DSHS-TestCrawler.git
# 或是下載 zip
cd DSHS-TestCrawler
python -m pip install -r requirements.txt
```

### 有還原卡的安裝

可以用 WinPython (待研究)