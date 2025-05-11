import streamlit as st
import datetime

# -- 設定: 閾値 --
HOPE_THRESHOLD = 3  # ホープがこの数押されたらイベント化
COPE_THRESHOLD = 2  # コープがこの数押されたらイベント化

# -- データのモック --
if "wants" not in st.session_state:
    st.session_state.wants = [
        {"title": "ハイキング企画", "owner": "Alice", "hope_count": 0, "cope_count": 0},
        {"title": "読書会",     "owner": "Bob",   "hope_count": 1, "cope_count": 0},
    ]
if "events" not in st.session_state:
    st.session_state.events = [
        {"title": "お花見",       "date": "2025-04-01"},
        {"title": "ボードゲーム会", "date": "2025-04-15"},
    ]
# コメントとチャットのログ
if "comment_logs" not in st.session_state:
    st.session_state.comment_logs = {0: [
        {"name": "佐藤", "message": "4月5日で集合はどうですか？"},
        {"name": "山田", "message": "別の日でも大丈夫です！"}
    ]}
if "chat_logs" not in st.session_state:
    st.session_state.chat_logs = {0: [
        {"name": "佐藤", "message": "お花見楽しみです！"},
        {"name": "山田", "message": "よろしくお願いします😊"}
    ]}
# 参加中イベントのインデックス管理
if "participating" not in st.session_state:
    st.session_state.participating = []  # イベントのインデックスリスト

if "profile" not in st.session_state:
    st.session_state.profile = {"name": "test_user", "email": ""}

# -- ページ状態 --
if "page" not in st.session_state:
    st.session_state.page = "トップ画面"

# -- ページ関数定義 --
def page_home():
    st.header("トップ画面")
    name = st.session_state.profile.get("name", "")
    st.write(f"こんにちは {name} さん")
    st.write("各機能へのリンク")
    if st.button("📋 ウォンツ一覧"): st.session_state.page = "ウォンツ一覧"; st.rerun()
    if st.button("🎉 イベント一覧"): st.session_state.page = "イベント一覧"; st.rerun()
    if st.button("👥 参加中イベント"): st.session_state.page = "参加中イベント"; st.rerun()
    if st.button("👤 プロフィール編集"): st.session_state.page = "プロフィール編集"; st.rerun()


def page_profile_edit():
    st.header("プロフィール編集")
    name = st.text_input("名前", st.session_state.profile.get("name", "test_user"))
    email = st.text_input("メールアドレス", st.session_state.profile.get("email", ""))
    if st.button("保存"): 
        st.session_state.profile.update({"name": name, "email": email})
        st.success("保存しました！")
    if st.button("← トップへ戻る"): st.session_state.page = "トップ画面"; st.rerun()


def page_wants_list():
    st.header("ウォンツ一覧")
    for i, w in enumerate(st.session_state.wants):
        info = f" (💡{w['hope_count']}/{HOPE_THRESHOLD} 🤝{w['cope_count']}/{COPE_THRESHOLD})"
        if st.button(f"🔍 {w['title']}{info}", key=f"want_{i}"):
            st.session_state.selected_idx = i; st.session_state.page = "ウォンツ詳細"; st.rerun()
    st.markdown("---")
    st.subheader("➕ 新規ウォンツ作成")
    title = st.text_input("イベント名", key="new_title")
    owner = st.text_input("開催者名", key="new_owner")
    if st.button("作成", key="create_want"): 
        st.session_state.wants.append({"title": title, "owner": owner, "hope_count": 0, "cope_count": 0})
        st.success("ウォンツを作成しました！")
        st.rerun()
    if st.button("← トップへ戻る"): st.session_state.page = "トップ画面"; st.rerun()


def page_want_detail():
    idx = st.session_state.selected_idx
    w = st.session_state.wants[idx]
    st.header(f"ウォンツ詳細：{w['title']}")
    st.write(f"- 開催者：{w['owner']}")
    st.write(f"💡 {w['hope_count']}/{HOPE_THRESHOLD}    🤝 {w['cope_count']}/{COPE_THRESHOLD}")
    if w['hope_count'] < HOPE_THRESHOLD:
        if st.button("💡 ホープ", key=f"hope_{idx}"):
            w['hope_count'] += 1
            if w['hope_count'] >= HOPE_THRESHOLD:
                st.session_state.events.append({"title": w['title'], "date": "未定(ホープ)"})
                st.session_state.selected_event = len(st.session_state.events) - 1
                st.session_state.wants.pop(idx)
                st.session_state.page = "イベント化完了"
            else:
                st.success(f"ホープ: {w['hope_count']}/{HOPE_THRESHOLD}")
            st.rerun()
    if w['cope_count'] < COPE_THRESHOLD:
        if st.button("🤝 コープ", key=f"cope_{idx}"):
            w['cope_count'] += 1
            if w['cope_count'] >= COPE_THRESHOLD:
                st.session_state.events.append({"title": w['title'], "date": "未定(コープ)"})
                st.session_state.selected_event = len(st.session_state.events) - 1
                st.session_state.wants.pop(idx)
                st.session_state.page = "イベント化完了"
            else:
                st.success(f"コープ: {w['cope_count']}/{COPE_THRESHOLD}")
            st.rerun()
    if st.button("← ウォンツ一覧へ戻る"): st.session_state.page = "ウォンツ一覧"; st.rerun()


def page_event_complete():
    e = st.session_state.events[st.session_state.selected_event]
    st.balloons()
    st.header("イベント化完了！")
    st.write(f"• タイトル: {e['title']}")
    st.write(f"• 日付: {e['date']}")
    if st.button("イベント一覧へ", key="to_list"): 
        st.session_state.page = "イベント一覧"
        st.rerun()
    if st.button("← トップへ戻る", key="home_from_events"):
        st.session_state.page = "トップ画面"
        st.rerun()


def page_events_list():
    st.header("イベント一覧")
    for j, e in enumerate(st.session_state.events):
        if st.button(f"🔍 {e['title']} ({e['date']})", key=f"event_{j}"):
            st.session_state.selected_event = j; st.session_state.page = "イベント詳細"; st.rerun()
    if st.button("← トップへ戻る", key="home_from_events"): st.session_state.page = "トップ画面"; st.rerun()


def page_event_detail():
    idx = st.session_state.selected_event
    e = st.session_state.events[idx]
    st.header(f"イベント詳細：{e['title']}")
    # 参加ボタン
    if idx not in st.session_state.participating:

        if st.button("🚀 参加する", key=f"join_{idx}"):
            st.session_state.participating.append(idx)
            st.session_state.page = "参加完了"
            st.rerun()
    try:
        default_date = datetime.datetime.strptime(e['date'], '%Y-%m-%d').date()
    except:
        default_date = datetime.date.today()
    new_date = st.date_input('日付設定', value=default_date, key=f'date_input_{idx}')
    if new_date.strftime('%Y-%m-%d') != e['date']:
        st.session_state.events[idx]['date'] = new_date.strftime('%Y-%m-%d')
        st.success('Date updated!')

    # コメントセクション（チャットスタイル）
    st.subheader("コメント")
    with st.container():
        if idx not in st.session_state.comment_logs:
            st.session_state.comment_logs[idx] = []
        for entry in st.session_state.comment_logs[idx]:
            st.chat_message(name=entry['name']).write(entry['message'])
        new_comment = st.chat_input("コメントを入力", key=f"comment_input_{idx}")
        if new_comment:
            user_name = st.session_state.profile.get("name", "User")
            st.session_state.comment_logs[idx].append({"name": user_name, "message": new_comment})
            st.rerun()



    if st.button('← イベント一覧へ戻る', key=f'back_event_{idx}'):
        st.session_state.page = 'イベント一覧'
        st.rerun()
    if st.button("← トップへ戻る", key="home_from_events"):
        st.session_state.page = "トップ画面"
        st.rerun()

def page_join_complete():
    idx = st.session_state.selected_event
    e = st.session_state.events[idx]
    st.balloons()
    st.header("参加完了！")
    st.write(f"「{e['title']}」に参加しました！")
    if st.button("参加中イベント一覧へ"):
        st.session_state.page = "参加中イベント"
        st.rerun()
    if st.button("← トップへ戻る", key="home_from_events"):
        st.session_state.page = "トップ画面"
        st.rerun()

def page_participating():
    st.header("参加中のイベント")
    if not st.session_state.participating:
        st.write("参加中のイベントはありません。イベント一覧から参加してください。")
    for idx in st.session_state.participating:
        e = st.session_state.events[idx]
        st.write(f"- {e['title']} ({e['date']})")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("詳細", key=f"part_detail_{idx}"):
                st.session_state.selected_event = idx
                st.session_state.page = "イベント詳細"
                st.rerun()
        with col2:
            if st.button("グループチャット", key=f"part_chat_{idx}"):
                st.session_state.selected_event = idx
                st.session_state.page = "参加チャット"
                st.rerun()
    if st.button("← トップへ戻る", key="home_from_part"):
        st.session_state.page = "トップ画面"
        st.rerun()


def page_participating_chat():
    idx = st.session_state.selected_event
    e = st.session_state.events[idx]
    st.header(f"グループチャット：{e['title']}")
    with st.container():
        if idx not in st.session_state.chat_logs:
            st.session_state.chat_logs[idx] = []
        for entry in st.session_state.chat_logs[idx]:
            st.chat_message(name=entry['name']).write(entry['message'])
        new_msg = st.chat_input("メッセージを入力", key=f"chat_input_{idx}")
        if new_msg:
            user_name = st.session_state.profile.get("name", "User")
            st.session_state.chat_logs[idx].append({"name": user_name, "message": new_msg})
            st.rerun()
    if st.button('← 参加中イベントへ戻る'):
        st.session_state.page = '参加中イベント'
        st.rerun()

# -- 遷移ロジック --
if st.session_state.page == "トップ画面": page_home()
elif st.session_state.page == "ウォンツ一覧": page_wants_list()
elif st.session_state.page == "ウォンツ詳細": page_want_detail()
elif st.session_state.page == "イベント化完了": page_event_complete()
elif st.session_state.page == "イベント一覧": page_events_list()
elif st.session_state.page == "イベント詳細": page_event_detail()
elif st.session_state.page == "参加完了": page_join_complete()
elif st.session_state.page == "参加中イベント": page_participating()
elif st.session_state.page == "参加チャット": page_participating_chat()
elif st.session_state.page == "プロフィール編集": page_profile_edit()
