# todo.py

# ★1. 定数の定義
# TODOリストのデータを保存するファイル名。JSON形式で保存します。
TODO_FILE = "todos.txt"

# ★JSONデータを扱うためのライブラリをインポート
import json


# ★2. 関数の定義 (display_todo_list)
def display_todo_list(todos):
    """
    TODOリストを表示する関数
    リストの中身が辞書になっていることを想定して表示します。
    """
    print("--- TODO リスト ---")
    if not todos:  # もしTODOリストが空っぽだったら
        print("TODOはありません。")
    else:  # TODOリストに項目があったら
        # for文でリストの各要素（todo_item = 辞書）を順番に取り出す
        for i, todo_item in enumerate(todos):
            # 辞書からタスク名と状態、期日を取得。get()はキーがなくてもエラーにならない安全な取得方法。
            task_name = todo_item.get("task", "不明なタスク")
            status = todo_item.get("status", "不明")

            # 状態表示の調整（pendingを「未完了」、completedを「完了」と表示）
            status_display = ""
            if status == "pending":
                status_display = "未完了"
            elif status == "completed":
                status_display = "✔"  # ここを「✔」に修正しました
            else:
                status_display = status  # 不明な場合はそのまま表示

            # 期日表示の調整（期日があれば表示に追加）
            due_date_str = todo_item.get("due_date", "")
            if due_date_str:  # 期日の文字列が空でなければ
                due_date_str = f" (期日: {due_date_str})"

            # 最終的な表示形式
            print(f"{i + 1}. [{status_display}] {task_name}{due_date_str}")
    print("--------------------")


# ★3. 関数の定義 (add_todo)
def add_todo(todos):
    """
    TODOを追加する関数
    新しいTODOを辞書として作成し、リストに追加します。
    """
    new_todo_task = input("新しいTODOを入力してください: ")

    # 各TODOは、'task'でタスク名、'status'で状態、'due_date'で期日を持つ辞書になります。
    new_todo_item = {
        "task": new_todo_task,
        "status": "pending",  # 初期状態は「未完了」
        "due_date": "",  # 初期状態は期日なし
    }
    todos.append(new_todo_item)  # 作成した辞書をTODOリストの最後に追加
    print(f"'{new_todo_task}' を追加しました。")


# ★4. 関数の定義 (delete_todo)
def delete_todo(todos):
    """
    TODOを削除する関数
    """
    if not todos:  # TODOリストが空っぽなら削除できない
        print("削除できるTODOはありません。")
        return  # この関数をここで終了

    display_todo_list(
        todos
    )  # ユーザーにどのTODOを削除するか選んでもらうために、リストを表示
    try:
        todo_index_str = input("削除するTODOの番号を入力してください: ")
        todo_index = (
            int(todo_index_str) - 1
        )  # ユーザー入力（1から始まる）をリストのインデックス（0から始まる）に変換

        if 0 <= todo_index < len(todos):  # 入力された番号が有効な範囲内かチェック
            deleted_todo_item = todos.pop(
                todo_index
            )  # 指定されたインデックスの辞書をリストから削除し、その辞書を取得
            # 削除メッセージのために、辞書からタスク名を取り出して表示
            print(f"'{deleted_todo_item.get('task', '不明なタスク')}' を削除しました。")
        else:  # 番号が無効な場合
            print("無効な番号です。リストに表示されている番号を入力してください。")
    except ValueError:  # 数字以外の文字が入力されたら
        print("数字を入力してください。")
    except Exception as e:  # その他のエラー
        print(f"エラーが発生しました: {e}")


# ★5. 関数の定義 (update_todo)
def update_todo(todos):
    """
    TODOを更新する関数
    タスク名、状態、期日を個別に更新できるようにします。
    """
    if not todos:  # TODOリストが空っぽなら更新できない
        print("更新できるTODOはありません。")
        return

    display_todo_list(
        todos
    )  # ユーザーにどのTODOを更新するか選んでもらうために、リストを表示
    try:
        todo_index_str = input("更新するTODOの番号を入力してください: ")
        todo_index = (
            int(todo_index_str) - 1
        )  # ユーザー入力からリストのインデックスに変換

        if 0 <= todo_index < len(todos):  # 番号が有効な範囲内かチェック
            current_todo_item = todos[todo_index]  # 更新対象のTODO（辞書）を取得
            print(f"現在のTODO: '{current_todo_item.get('task', '不明なタスク')}'")

            # 更新する項目をユーザーに選んでもらうメニュー
            print("更新する項目を選んでください:")
            print("1. タスク名")
            print("2. 状態 (完了/未完了)")
            print("3. 期日")
            update_choice = input("選択してください (1/2/3): ")

            if update_choice == "1":  # タスク名を更新
                new_task_content = input(
                    f"新しいタスク名を入力してください (現在の内容: '{current_todo_item.get('task', '')}'): "
                )
                current_todo_item["task"] = (
                    new_task_content  # 辞書の'task'キーの値を更新
                )
                print(f"タスク名を '{new_task_content}' に更新しました。")
            elif update_choice == "2":  # 状態を更新
                new_status = input(
                    f"新しい状態を入力してください (pending:未完了 / completed:完了) (現在の状態: '{current_todo_item.get('status', '')}'): "
                ).lower()
                if new_status in ["pending", "completed"]:  # 有効な状態かチェック
                    current_todo_item["status"] = (
                        new_status  # 辞書の'status'キーの値を更新
                    )
                    print(f"状態を '{new_status}' に更新しました。")
                else:
                    print(
                        "無効な状態です。'pending' または 'completed' を入力してください。"
                    )
            elif update_choice == "3":  # 期日を更新
                new_due_date = input(
                    f"新しい期日を入力してください (YYYY-MM-DD形式、空欄で期日なし) (現在の期日: '{current_todo_item.get('due_date', '')}'): "
                )
                current_todo_item["due_date"] = (
                    new_due_date  # 辞書の'due_date'キーの値を更新
                )
                print(f"期日を '{new_due_date}' に更新しました。")
            else:  # 無効な選択
                print("無効な選択です。")

            # current_todo_itemは辞書なので、直接変更すればtodosリスト内の辞書も更新されます。
            # todos[todo_index] = current_todo_item と再代入しても問題ありません。

        else:  # 番号が無効な場合
            print("無効な番号です。リストに表示されている番号を入力してください。")
    except ValueError:
        print("数字を入力してください。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")


# ★6. 関数の定義 (load_todos) - JSON形式に対応
def load_todos(filename):
    """
    ファイルからTODOをJSON形式で読み込む関数
    """
    todos = []  # まずは空のリストを用意
    try:
        with open(
            filename, "r", encoding="utf-8"
        ) as f:  # ファイルを読み込みモードで開く
            todos = json.load(
                f
            )  # json.load()でファイルの内容を読み込み、Pythonのリストや辞書に変換
        print(f"TODOリストを {filename} から読み込みました。")
    except FileNotFoundError:  # ファイルが見つからない場合（初回起動など）
        print(f"情報: {filename} が見つかりません。新しいTODOリストを作成します。")
    except json.JSONDecodeError:  # ファイルの内容がJSONとして不正な場合
        print(
            f"警告: {filename} の内容が不正なJSON形式です。新しいTODOリストを作成します。"
        )
    except Exception as e:  # その他のエラー
        print(f"TODOの読み込み中にエラーが発生しました: {e}")
    return todos  # 読み込んだリスト（または空のリスト）を返す


# ★7. 関数の定義 (save_todos) - JSON形式に対応
def save_todos(todos, filename):
    """
    TODOをファイルにJSON形式で保存する関数
    """
    try:
        with open(
            filename, "w", encoding="utf-8"
        ) as f:  # ファイルを書き込みモードで開く（既存内容は上書き）
            # json.dump()でPythonのリストや辞書をJSON形式の文字列に変換してファイルに書き込む
            # indent=4でJSONを見やすく字下げ、ensure_ascii=Falseで日本語がそのまま保存される
            json.dump(todos, f, indent=4, ensure_ascii=False)
        print(f"TODOリストを {filename} に保存しました。")
    except Exception as e:  # エラー処理
        print(f"TODOの保存中にエラーが発生しました: {e}")


# ★8. アプリケーションの開始 (メインの実行部分)
# --- アプリケーションの開始 ---
# アプリが起動したときに、ここから処理が始まります。

# アプリ起動時、TODOリストをファイルから読み込む
my_todos = load_todos(TODO_FILE)

print("\nアプリケーションを開始します。")
display_todo_list(my_todos)  # 最初に現在のTODOリスト（読み込んだ内容）を表示

while True:  # このループの中の処理が、アプリが終了するまでずっと繰り返されます
    print("\n--- メニュー ---")
    print("1. TODOを追加")
    print("2. TODOを表示")
    print("3. TODOを削除")
    print("4. TODOを更新")
    print("5. アプリを終了")
    print(
        "6. （オプション）TODOの状態を変更する"
    )  # 状態変更は「4」の更新で可能ですが、メニューを維持
    choice = input("選択してください (1/2/3/4/5/6): ")

    if choice == "1":  # ユーザーが「1」を選んだら
        add_todo(my_todos)
    elif choice == "2":  # ユーザーが「2」を選んだら
        display_todo_list(my_todos)
    elif choice == "3":  # ユーザーが「3」を選んだら
        delete_todo(my_todos)
    elif choice == "4":  # ユーザーが「4」を選んだら
        update_todo(my_todos)
    elif choice == "5":  # ユーザーが「5」を選んだら（アプリ終了）
        save_todos(my_todos, TODO_FILE)  # 終了前にTODOリストをファイルに保存
        print("TODOアプリを終了します。")
        break  # whileループを終了させ、アプリを閉じる
    elif choice == "6":  # ユーザーが「6」を選んだら
        print("update_todo (4) を使って状態を変更してください。")
    else:  # ユーザーが無効な選択をしたら
        print("無効な選択です。1, 2, 3, 4, 5, 6 のいずれかを入力してください。")
