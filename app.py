# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import os
#
# # 定义数据存储的文件名
# DATA_FILE = "attendance_records.csv"
#
#
# # 【功能函数】读取历史记录
# def load_data():
#     if os.path.exists(DATA_FILE):
#         return pd.read_csv(DATA_FILE)
#     else:
#         # 如果文件不存在，创建一个空的DataFrame，定义好列名
#         return pd.DataFrame(columns=["日期", "上班时间", "下班时间", "工作时长(小时)"])
#
#
# # 【功能函数】保存数据
# def save_data(df):
#     df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
#
#
# # --- 网页界面设计 ---
#
# # 设置网页标题
# st.title("⏱️ 个人上下班打卡工具")
#
# # 获取系统当前时间和日期
# now = datetime.now()
# today_str = now.strftime("%Y-%m-%d")
# time_str = now.strftime("%H:%M:%S")
#
# st.write(f"**今天是:** {today_str} | **当前系统时间:** {time_str}")
#
# # 加载数据
# df = load_data()
#
# # 检查今天是否已经有打卡记录
# today_record_index = df[df["日期"] == today_str].index
#
# # 界面布局：分成两列放两个按钮
# col1, col2 = st.columns(2)
#
# with col1:
#     if st.button("🟢 上班打卡", use_container_width=True):
#         if len(today_record_index) > 0:
#             st.warning("今天已经打过上班卡啦！")
#         else:
#             # 添加一条新记录
#             new_record = pd.DataFrame([{
#                 "日期": today_str,
#                 "上班时间": time_str,
#                 "下班时间": "",
#                 "工作时长(小时)": ""
#             }])
#             df = pd.concat([df, new_record], ignore_index=True)
#             save_data(df)
#             st.success(f"上班打卡成功！时间：{time_str}")
#             st.rerun()  # 刷新页面更新数据
#
# with col2:
#     if st.button("🔴 下班打卡", use_container_width=True):
#         if len(today_record_index) == 0:
#             st.error("你今天还没打上班卡，不能直接打下班卡哦！")
#         else:
#             # 找到今天的记录
#             idx = today_record_index[0]
#             if df.loc[idx, "下班时间"] != "":
#                 st.warning("今天已经打过下班卡啦！如果重复打卡将覆盖之前的时间。")
#
#             # 记录下班时间
#             df.loc[idx, "下班时间"] = time_str
#
#             # 计算工作时长
#             start_time_str = df.loc[idx, "上班时间"]
#             start_time = datetime.strptime(f"{today_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
#             end_time = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")
#
#             # 计算时间差，转换为小时（保留两位小数）
#             duration = (end_time - start_time).total_seconds() / 3600
#             df.loc[idx, "工作时长(小时)"] = round(duration, 2)
#
#             save_data(df)
#             st.success(f"下班打卡成功！今天工作了 {round(duration, 2)} 小时。辛苦了！")
#             st.rerun()  # 刷新页面
#
# st.divider()  # 分割线
#
# # --- 历史记录查询模块 ---
# st.subheader("📅 历史打卡记录查询")
#
# # 提供一个按键，点击后展开历史记录
# if st.checkbox("查看所有打卡记录"):
#     if df.empty:
#         st.info("目前还没有任何打卡记录。")
#     else:
#         # 在网页上展示表格
#         st.dataframe(df, use_container_width=True)
#
#         # 计算一下总工作时长和平均工作时长（进阶小功能）
#         total_hours = pd.to_numeric(df["工作时长(小时)"], errors='coerce').sum()
#         st.write(f"**累计工作总时长:** {total_hours} 小时")


# import streamlit as st
# import pandas as pd
# from datetime import datetime, timezone, timedelta
# import os
#
# DATA_FILE = "attendance_records.csv"
#
#
# # --- 功能函数 ---
# def load_data():
#     if os.path.exists(DATA_FILE):
#         df = pd.read_csv(DATA_FILE)
#         # 防止读取CSV时空白变成 NaN 导致报错，把空值统一转换为空字符串
#         df["下班时间"] = df["下班时间"].fillna("")
#         df["工作时长(小时)"] = df["工作时长(小时)"].fillna("")
#         return df
#     else:
#         return pd.DataFrame(columns=["日期", "上班时间", "下班时间", "工作时长(小时)"])
#
#
# def save_data(df):
#     df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
#
#
# # --- 时区设置 ---
# # 强制使用北京时间 (UTC+8)
# tz_beijing = timezone(timedelta(hours=8))
#
# # 获取正确的北京时间和日期
# now = datetime.now(tz_beijing)
# today_str = now.strftime("%Y-%m-%d")
# time_str = now.strftime("%H:%M:%S")
#
# # --- 网页界面设计 ---
# st.title("⏱️ 个人上下班打卡工具")
# st.write(f"**今天是:** {today_str} | **当前系统时间 (北京时间):** {time_str}")
#
# df = load_data()
#
# # 寻找所有【未打下班卡】的记录
# uncompleted_records = df[df["下班时间"] == ""]
#
# col1, col2 = st.columns(2)
#
# # --- 上班打卡逻辑 ---
# with col1:
#     if st.button("🟢 上班打卡", use_container_width=True):
#         if len(uncompleted_records) > 0:
#             st.warning("您还有尚未结束的打卡记录，请先打下班卡！")
#         else:
#             new_record = pd.DataFrame([{
#                 "日期": today_str,
#                 "上班时间": time_str,
#                 "下班时间": "",
#                 "工作时长(小时)": ""
#             }])
#             df = pd.concat([df, new_record], ignore_index=True)
#             save_data(df)
#             st.success(f"上班打卡成功！时间：{time_str}")
#             st.rerun()
#
# # --- 下班打卡逻辑 (已修复跨天计算) ---
# with col2:
#     if st.button("🔴 下班打卡", use_container_width=True):
#         if len(uncompleted_records) == 0:
#             st.error("您还没有正在进行的上班记录，不能直接打下班卡哦！")
#         else:
#             # 找到最后一条未完成的记录的索引
#             idx = uncompleted_records.index[-1]
#
#             # 记录下班时间
#             df.loc[idx, "下班时间"] = time_str
#
#             # 获取它上班那天的日期和时间
#             start_date_str = df.loc[idx, "日期"]
#             start_time_str = df.loc[idx, "上班时间"]
#
#             # 组合成完整的日期时间对象进行精确计算 (不管跨了多少天都不怕)
#             start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
#             end_datetime = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")
#
#             # 计算时长
#             duration = (end_datetime - start_datetime).total_seconds() / 3600
#
#             # 容错处理：如果你之前测试出了负数，这里清零，防止显示错误
#             if duration < 0:
#                 duration = 0
#
#             df.loc[idx, "工作时长(小时)"] = round(duration, 2)
#
#             save_data(df)
#             st.success(f"下班打卡成功！本次工作了 {round(duration, 2)} 小时。")
#             st.rerun()
#
# st.divider()
#
# # --- 历史记录查询模块 ---
# st.subheader("📅 历史打卡记录查询")
#
# if st.checkbox("查看所有打卡记录"):
#     if df.empty:
#         st.info("目前还没有任何打卡记录。")
#     else:
#         st.dataframe(df, use_container_width=True)
#         # 计算时排除空值和负数（防止之前的错误数据影响总计）
#         valid_hours = pd.to_numeric(df["工作时长(小时)"], errors='coerce')
#         total_hours = valid_hours[valid_hours > 0].sum()
#         st.write(f"**累计有效工作总时长:** {round(total_hours, 2)} 小时")


# import streamlit as st
# import pandas as pd
# from datetime import datetime, timezone, timedelta
# import os
#
# DATA_FILE = "attendance_records.csv"
#
#
# # --- 功能函数 ---
# def load_data():
#     if os.path.exists(DATA_FILE):
#         df = pd.read_csv(DATA_FILE)
#         df["下班时间"] = df["下班时间"].fillna("")
#         df["工作时长(小时)"] = df["工作时长(小时)"].fillna("")
#         return df
#     else:
#         return pd.DataFrame(columns=["日期", "上班时间", "下班时间", "工作时长(小时)"])
#
#
# def save_data(df):
#     df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')
#
#
# # --- 时区与时间设置 ---
# tz_beijing = timezone(timedelta(hours=8))
# now = datetime.now(tz_beijing)
# today_str = now.strftime("%Y-%m-%d")
# time_str = now.strftime("%H:%M:%S")
#
# # --- 网页界面设计 ---
# st.title("⏱️ 个人上下班打卡工具")
# st.write(f"**今天是:** {today_str} | **当前系统时间 (北京时间):** {time_str}")
#
# df = load_data()
#
# # 检查今天是否已经打过上班卡
# has_punched_in_today = not df[df["日期"] == today_str].empty
#
# col1, col2 = st.columns(2)
#
# # --- 🟢 上班打卡逻辑 (每日限1次) ---
# with col1:
#     if st.button("🟢 上班打卡", use_container_width=True):
#         if has_punched_in_today:
#             # 如果今天已经有记录了，阻止再次生成新行
#             st.warning("您今天已经打过上班卡啦！安心工作吧。")
#         else:
#             # 只有今天没打过卡，才新建一行
#             new_record = pd.DataFrame([{
#                 "日期": today_str,
#                 "上班时间": time_str,
#                 "下班时间": "",
#                 "工作时长(小时)": ""
#             }])
#             df = pd.concat([df, new_record], ignore_index=True)
#             save_data(df)
#             st.success(f"上班打卡成功！时间：{time_str}")
#             st.rerun()
#
# # --- 🔴 下班打卡逻辑 (可无限次更新最新时间) ---
# with col2:
#     if st.button("🔴 下班打卡", use_container_width=True):
#         if df.empty:
#             st.error("系统没有任何上班记录，无法打下班卡！")
#         else:
#             # 永远抓取表格的最后一行（最新的一次工作记录）
#             idx = df.index[-1]
#
#             # 获取它上班那天的日期和时间
#             start_date_str = df.loc[idx, "日期"]
#             start_time_str = df.loc[idx, "上班时间"]
#
#             # 更新为最新的下班时间
#             df.loc[idx, "下班时间"] = time_str
#
#             # 计算时长
#             start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
#             end_datetime = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")
#
#             duration = (end_datetime - start_datetime).total_seconds() / 3600
#             if duration < 0: duration = 0
#
#             df.loc[idx, "工作时长(小时)"] = round(duration, 2)
#
#             save_data(df)
#             st.success(f"下班时间已更新！本次工作了 {round(duration, 2)} 小时。辛苦了！")
#             st.rerun()
#
# st.divider()
#
# # --- 历史记录查询模块 ---
# st.subheader("📅 历史打卡记录查询")
#
# if st.checkbox("查看所有打卡记录"):
#     if df.empty:
#         st.info("目前还没有任何打卡记录。")
#     else:
#         st.dataframe(df, use_container_width=True)
#         # 计算时排除空值和负数
#         valid_hours = pd.to_numeric(df["工作时长(小时)"], errors='coerce')
#         total_hours = valid_hours[valid_hours > 0].sum()
#         st.write(f"**累计有效工作总时长:** {round(total_hours, 2)} 小时")


import streamlit as st
import pandas as pd
from datetime import datetime, timezone, timedelta
from supabase import create_client, Client


# --- 初始化云端数据库连接 ---
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


supabase: Client = init_connection()


# --- 数据库读写功能函数 ---
def load_data():
    # 从云端数据库抓取 records 表的所有数据，按 id 排序
    response = supabase.table('records').select('*').order('id', desc=False).execute()
    df = pd.DataFrame(response.data)
    if not df.empty:
        df["end_time"] = df["end_time"].fillna("")
        df["duration"] = df["duration"].fillna(0.0)
    return df


# --- 时区与时间设置 ---
tz_beijing = timezone(timedelta(hours=8))
now = datetime.now(tz_beijing)
today_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M:%S")

# --- 网页界面设计 ---
st.title("⏱️ ClockIn")
st.write(f"**今天是:** {today_str} | **当前系统时间:** {time_str}")

# 加载云端数据
df = load_data()

# 检查今天是否已经打过上班卡
has_punched_in_today = False
if not df.empty:
    has_punched_in_today = not df[df["date"] == today_str].empty

col1, col2 = st.columns(2)

# --- 🟢 上班打卡 (向云端 Insert 数据) ---
with col1:
    if st.button("🟢 上班打卡", use_container_width=True):
        if has_punched_in_today:
            st.warning("您今天已经打过上班卡啦！安心工作吧。")
        else:
            # 向数据库插入新记录
            supabase.table('records').insert({
                "date": today_str,
                "start_time": time_str,
                "end_time": "",
                "duration": 0.0
            }).execute()

            st.success(f"上班打卡成功！时间：{time_str} (已同步至云端)")
            st.rerun()

# --- 🔴 下班打卡 (向云端 Update 数据) ---
with col2:
    if st.button("🔴 下班打卡", use_container_width=True):
        if df.empty:
            st.error("系统没有任何上班记录，无法打下班卡！")
        else:
            # 找到数据库中的最后一条记录
            last_record = df.iloc[-1]
            record_id = int(last_record['id'])
            start_date_str = last_record['date']
            start_time_str = last_record['start_time']

            # 计算时长
            start_datetime = datetime.strptime(f"{start_date_str} {start_time_str}", "%Y-%m-%d %H:%M:%S")
            end_datetime = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")
            duration = (end_datetime - start_datetime).total_seconds() / 3600
            if duration < 0: duration = 0

            # 更新数据库里的对应记录
            supabase.table('records').update({
                "end_time": time_str,
                "duration": round(duration, 2)
            }).eq("id", record_id).execute()

            st.success(f"下班时间已更新！本次工作了 {round(duration, 2)} 小时。")
            st.rerun()

st.divider()

# --- 历史记录查询模块 ---
st.subheader("📅 历史打卡记录查询")

if st.checkbox("查看所有打卡记录"):
    if df.empty:
        st.info("云端数据库目前还没有任何记录。")
    else:
        # 为了展示美观，把英文列名重命名为中文
        display_df = df[['date', 'start_time', 'end_time', 'duration']].rename(columns={
            'date': '日期',
            'start_time': '上班时间',
            'end_time': '下班时间',
            'duration': '工作时长(小时)'
        })
        st.dataframe(display_df, use_container_width=True)

        valid_hours = pd.to_numeric(df["duration"], errors='coerce')
        total_hours = valid_hours[valid_hours > 0].sum()
        st.write(f"**累计有效工作总时长:** {round(total_hours, 2)} 小时")