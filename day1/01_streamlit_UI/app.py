import streamlit as st
import pandas as pd
import datetime

st.title("睡眠に関するアンケート")
st.markdown("あなたの睡眠データを記録します")

# --------------------------------------------------
# 睡眠時間の記録
# --------------------------------------------------
st.header("1. 睡眠時間の記録")
if 'sleep_data' not in st.session_state:
    st.session_state['sleep_data'] = pd.DataFrame(columns=['日付', '睡眠時間'])

record_date = st.date_input("記録する日付", datetime.date.today())
sleep_time = st.slider("睡眠時間（時間）", 0.0, 12.0, 7.0, 0.5)

if st.button("睡眠時間を記録"):
    # 既存のデータに同じ日付のレコードがあるか確認
    existing_record = st.session_state['sleep_data'][st.session_state['sleep_data']['日付'] == record_date]
    if not existing_record.empty:
        st.warning(f"{record_date} の記録はすでに存在します。上書きしますか？")
        if st.button("上書きする"):
            st.session_state['sleep_data'].loc[st.session_state['sleep_data']['日付'] == record_date, '睡眠時間'] = sleep_time
            st.success(f"{record_date} の睡眠時間を {sleep_time} 時間に更新しました！")
    else:
        new_record = pd.DataFrame({'日付': [record_date], '睡眠時間': [sleep_time]})
        st.session_state['sleep_data'] = pd.concat([st.session_state['sleep_data'], new_record], ignore_index=True)
        st.success(f"{record_date} の睡眠時間 {sleep_time} 時間を記録しました！")

if not st.session_state['sleep_data'].empty:
    st.subheader("過去の睡眠時間")
    # 日付でソートして表示
    st.dataframe(st.session_state['sleep_data'].sort_values(by='日付', ascending=False))

    st.subheader("睡眠時間の推移")
    st.line_chart(st.session_state['sleep_data'].set_index('日付'))
else:
    st.info("まだ睡眠時間が記録されていません。")

st.divider()

# --------------------------------------------------
# 睡眠の質に関する質問
# --------------------------------------------------
st.header("2. 睡眠の質に関する質問")
quality = st.radio(
    "昨晩の睡眠の質を評価してください",
    ['とても良い', '良い', '普通', '悪い', 'とても悪い']
)
st.session_state['quality'] = quality

disturbances = st.multiselect(
    "昨晩、睡眠を妨げる要因はありましたか？ (複数選択可)",
    ['寝る前のスマートフォン', 'カフェイン摂取', '騒音', '部屋の明るさ', 'その他']
)
st.session_state['disturbances'] = disturbances

free_text = st.text_area("睡眠の質について何か気になることがあれば記述してください")
st.session_state['free_text'] = free_text

st.divider()

# --------------------------------------------------
# 起床時の状態に関する質問
# --------------------------------------------------
st.header("3. 起床時の状態に関する質問")
mood = st.radio(
    "今朝の起床時の気分はどうでしたか？",
    ['とても良い', '良い', '普通', '悪い', 'とても悪い']
)
st.session_state['mood'] = mood

tiredness = st.slider("起床時のだるさを評価してください (0: 全くない - 10: 非常にだるい)", 0, 10, 5)
st.session_state['tiredness'] = tiredness

st.divider()

# --------------------------------------------------
# 睡眠環境に関する質問
# --------------------------------------------------
st.header("4. 睡眠環境に関する質問")
temperature = st.selectbox(
    "寝室の温度はどのくらいでしたか？",
    ['少し寒い', '適温', '少し暑い', '暑い', '寒い']
)
st.session_state['temperature'] = temperature

noise = st.checkbox("寝室に気になる騒音はありましたか？")
st.session_state['noise'] = noise

light = st.checkbox("寝室は十分に暗かったですか？")
st.session_state['light'] = light

st.divider()

# --------------------------------------------------
# 回答の表示 (オプション)
# --------------------------------------------------
st.subheader("回答内容 (確認用)")
st.write("---")
st.write(f"**記録日:** {record_date}")
st.write(f"**昨晩の睡眠時間:** {sleep_time} 時間")
st.write(f"**睡眠の質の評価:** {st.session_state.get('quality', '')}")
if st.session_state.get('disturbances'):
    st.write(f"**睡眠を妨げた要因:** {', '.join(st.session_state.get('disturbances', []))}")
if st.session_state.get('free_text'):
    st.write(f"**睡眠の質に関するコメント:** {st.session_state.get('free_text', '')}")
st.write(f"**起床時の気分:** {st.session_state.get('mood', '')}")
st.write(f"**起床時のだるさ:** {st.session_state.get('tiredness', '')}")
st.write(f"**寝室の温度:** {st.session_state.get('temperature', '')}")
st.write(f"**気になる騒音:** {'あり' if st.session_state.get('noise') else 'なし'}")
st.write(f"**部屋の明るさ:** {'十分な暗さ' if st.session_state.get('light') else '明るい'}")

st.markdown("ご協力ありがとうございました！")