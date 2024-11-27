import requests
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


def get_contribution_data(username, token):
    query = """
    query {
      user(login: "%s") {
        contributionsCollection {
          contributionCalendar {
            weeks {
              contributionDays {
                date
                contributionCount
              }
            }
          }
        }
      }
    }
    """ % username
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]


def generate_contribution_heatmap(weeks):
    # 解析贡献数据
    contributions = []
    for week in weeks:
        for day in week["contributionDays"]:
            contributions.append({
                "date": datetime.strptime(day["date"], "%Y-%m-%d"),
                "count": day["contributionCount"]
            })

    # 创建 DataFrame
    df = pd.DataFrame(contributions)
    df['week'] = df['date'].dt.isocalendar().week
    df['weekday'] = df['date'].dt.weekday

    # 构建矩阵 (行: 周, 列: 星期)
    pivot = df.pivot("weekday", "week", "count").fillna(0)

    # 绘制热力图
    plt.figure(figsize=(15, 5))
    sns.heatmap(pivot, cmap="Greens", linewidths=0.1, linecolor="white", cbar=True, square=True)

    # 配置轴
    plt.title("GitHub Contributions Heatmap", fontsize=16)
    plt.xlabel("Week of Year", fontsize=12)
    plt.ylabel("Day of Week", fontsize=12)
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(
        [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5],
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        rotation=0,
        fontsize=10
    )
    
    # 保存图片
    plt.tight_layout()
    plt.savefig("contributions.png")
    plt.close()


if __name__ == "__main__":
    username = "MingcanYang"  # 替换为您的 GitHub 用户名
    token = os.getenv("PAT_TOKEN")  # 从环境变量中读取 Personal Access Token
    if not token:
        raise ValueError("PAT_TOKEN is not set. Please check your workflow environment.")
    weeks = get_contribution_data(username, token)
    generate_contribution_heatmap(weeks)
