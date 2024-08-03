# このリポジトリについて
## 概要

以下のページのFastAPIでToDoアプリを作るチュートリアルについてのrepositoryです。
https://rightcode.co.jp/blogs/8708

2019年に作られていて文法がやや古いため、エラーになる部分あったり
誤記があったりするため、実際に動くコードをアップロードしています。また、記事に沿ってコーディングした際のエラー解消方法をReadme記載しています。

## 本リポジトリの動かし方

- リポジトリをクローン
``` bash
git clone https://github.com/shinji-kodama/techpit-fastapi-todo-tutorial.git
```
- pythonの仮想環境を作成して使用

windowsの場合
``` bash
cd techpit-fastapi-todo-tutorial
python -m venv .venv
.\.venv\Scripts\activate
```
Linux, Macの場合
``` bash
cd techpit-fastapi-todo-tutorial
python -m venv .venv
source ./.venv/bin/activate
```

- requirements.txtを用いてライブラリを一括インストール
``` bash
pip install -r requrements.txt
```

- run.pyを実行
``` bash
python run.py
```


# エラー解消方法
## 第１回
### controllers.pyに加筆

最後に閉じカッコが足りない

### templates/layout.html

- jinja2はインストールが必要  

インストールしないと動かないので  
以下のコマンドを打ちましょう

``` bash
pip install jinja2
```

- サーバー起動するとエラになる場合

「何もメインコンテンツがないと、以下のような見た目です。」と記述がありますが
まだindex.htmlが無いためサーバーを起動してもエラーになります。  
index.htmlを作成後、サーバーを起動してみてください


## 第2回

### 実装してみる (models.py)

Pydantic使ってないのか  
どうしよう

### 管理者ページのコントローラを修正する

以下の場所でエラーが出るはず
``` python
def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
```

securityの定義をしていないためなので
以下のようにsecurityを定義してあげる
``` python

import hashlib 

security = HTTPBasic()

app = FastAPI(
    ...
)
```

### ビューを作る

少し前の項に書いてありますが、
templates/resiter.htmlを作成してその中にhtmlを記述してください


### POSTメソッド処理を書く

request.form()でエラーが出た場合は、`import urllib.parse`を書き加えて、更に以下のように書き換えてください

``` python
    if request.method == 'POST':
        # POSTデータ
        data = await request.form()
        username = data.get('username')
        password = data.get('password')
        password_tmp = data.get('password_tmp')
        mail = data.get('mail')
```
↓
``` python

    if request.method == 'POST':
        # POSTデータ
        request_body = await request.body()
        data = urllib.parse.parse_qs(request_body.decode())
        
        username, = data.get('username') # コンマが増えているので注意
        password, = data.get('password') # コンマが増えているので注意
        password_tmp, = data.get('password_tmp') # コンマが増えているので注意
        mail, = data.get('mail') # コンマが増えているので注意
```



### 登録完了のビューをつくる

直前で書いたcontrollerの記述を見れば自明ですはありますが、
templatesフォルダ内にcomplete.htmlというファイルを作って登録完了の画面の中身を記述しましょう

## 第4回
### MyCalendarクラス

以下の記述の`ja_jp`の部分を`ja_JP.UTF-8`と書き換えるか、空文字にしましょう

``` python
def __init__(self, username, linked_date: dict):
    calendar.LocaleHTMLCalendar.__init__(self,
                                         firstweekday=6,
                                         locale='ja_jp')
```

### adminコントローラを修正する

timedeltaがimportされてないのでimportしてから使いましょう
``` python
from mycalendar import MyCalendar
from datetime import datetime, timedelta # timedeltaを追記
```

### 動作確認

- locale.Error: unsupported locale setting
`locale.Error: unsupported locale setting`というエラーが出る場合、少し戻って
MyCalendarクラスの記述を見てください。
エラーの解消方法が書いてあります。

- カレンダーに予定が表示されない

dbのtaskテーブル内のデータを確認してみてください。
deadlineが2019年のものしか登録されていないのではないでしょうか。

もし、カレンダー上にデータを登録したい場合、deadlineを明日の日付にして
データを登録してみてください。

sqliteを立ち上げて、以下のように打ってみましょう。（日付は変えてください）
``` sql
insert into task (user_id,content,deadline,date,done)
values(1,'test_test',datetime('2024-08-05'),datetime('2024-08-04'),0);
```

## 第5回

### /done をコーディングする

- `405 Method Not Allowed` がでる

RedirectResponseのstatus codeが307なのが原因です。
とりあえず回避するために、`from fastapi import status`をファイルの上部に追加してから  
controllers.pyのdoneメソッドを少し書き換えましょう。


``` python
 
    return RedirectResponse('/admin',
                            status_code=status.HTTP_303_SEE_OTHER) 
```

## 第6回

### /addをコーディング

これまでに出てきたのと同様、request.form()は使えないので  
以下のようにrequest.body()を使います。

また、RedirectResponseも出てきますので、status codeの変更を全章と同様に行ってください。

``` python
    # フォームからデータを取得
    request_body = await request.body() # form()をbody() に変更
    data = urllib.parse.parse_qs(request_body.decode())  # この行を追加
    year = int(data['year'][0])     # [0]を追加
    month = int(data['month'][0])   # [0]を追加
    day = int(data['day'][0])       # [0]を追加
    hour = int(data['hour'][0])     # [0]を追加
    minute = int(data['minute'][0]) # [0]を追加

    deadline = datetime(year=year, month=month, day=day,
                        hour=hour, minute=minute)

    # 新しくタスクを生成しコミット
    task = Task(user.id, data['content'][0], deadline) # [0]を追加
    db.session.add(task)
    db.session.commit()
    db.session.close()

```



また、上記のように year, month, dayを受け取っていますが、
教材中ではPOSTのデータにそれらが含まれていませんので、
detail.htmlの/add向けのform内にも以下のinputタグを追記してください

``` html
    <input type="hidden" name="year" value="{{ year }}">
    <input type="hidden" name="month" value="{{ month }}">
    <input type="hidden" name="day" value="{{ day }}">
```

### /delete/{task_id}のコントローラを書く

ここも同様にPOSTのデータを受け取って利用しています。
既出のrequest.form()をrequest.body()に書き換える方法で対応しましょう。

また、RediretResponseも出てきていますので、
同様にstatus codeを303にしてredirectしましょう。