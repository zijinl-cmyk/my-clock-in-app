import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 定义数据存储的文件名
DATA_FILE = "attendance_records.csv"


# 【功能函数】读取历史记录
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # 如果文件不存在，创建一个空的DataFrame，定义好列名
        return pd.DataFrame(columns=["日期", "上班时间", "下班时间", "工作时长(小时)"])


# 【功能函数】保存数据
def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')


# --- 网页界面设计 ---

# 设置网页标题
st.title("⏱️ 个人上下班打卡工具")

# 获取系统当前时间和日期
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

st.write(f"**今天是:** {today_str} | **当前系统时间:** {time_str}")

# 加载数据
df = load_data()

# 检查今天是否已经有打卡记录
today_record_index = df[df["日期"] == today_str].index

# 界面布局：分成两列放两个按钮
col1, col2 = st.columns(2)

with col1:
    if st.button("🟢 上班打卡", use_container_width=True):
        if len(today_record_index) > 0:
            st.warning("今天已经打过上班卡啦！")
        else:
            # 添加一条新记录
            new_record = pd.DataFrame([{
                "日期": today_str,
                "上班时间": time_str,
                "下班时间": "",
                "工作时长(小时)": ""
            }])
            df = pd.concat([df, new_record], ignore_index=True)
            save_data(df)
            st.success(f"上班打卡成功！时间：{time_str}")
            st.rerun()  # 刷新页面更新数据

with col2:
    if st.button("🔴 下班打卡", use_container_width=True):
        if len(today_record_index) == 0:
            st.error("你今天还没打上班卡，不能直接打下班卡哦！")
        else:
            # 找到今天的记录
            idx = today_record_index[0]
            if df.loc[idx, "下班时间"] != "":
                st.warning("今天已经打过下班卡啦！如果重复打卡将覆盖之前的时间。")

            # 记录下班时间
            df.loc[idx, "下班时间"] = time_str

            # 计算工作时长
            start_time_str = df.loc[idx, "上班时间"]
            start_time = datetime.strptime(f"{today_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")

            # 计算时间差，转换为小时（保留两位小数）
            duration = (end_time - start_time).total_seconds() / 3600
            df.loc[idx, "工作时长(小时)"] = round(duration, 2)

            save_data(df)
            st.success(f"下班打卡成功！今天工作了 {round(duration, 2)} 小时。辛苦了！")
            st.rerun()  # 刷新页面

st.divider()  # 分割线

# --- 历史记录查询模块 ---
st.subheader("📅 历史打卡记录查询")

# 提供一个按键，点击后展开历史记录
if st.checkbox("查看所有打卡记录"):
    if df.empty:
        st.info("目前还没有任何打卡记录。")
    else:
        # 在网页上展示表格
        st.dataframe(df, use_container_width=True)

        # 计算一下总工作时长和平均工作时长（进阶小功能）
        total_hours = pd.to_numeric(df["工作时长(小时)"], errors='coerce').sum()
        st.write(f"**累计工作总时长:** {total_hours} 小时")