import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # 用于日期格式化
import os
import datetime


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


def generate_contribution_image(weeks):
    dates = []
    counts = []
    for week in weeks:
        for day in week["contributionDays"]:
            dates.append(datetime.datetime.strptime(day["date"], "%Y-%m-%d"))
            counts.append(day["contributionCount"])

    fig, ax = plt.subplots(figsize=(15, 5))
    scatter = ax.scatter(dates, [0] * len(dates), c=counts, cmap="Greens", s=100, edgecolor="k", linewidth=0.5)

    # 配置 y 轴
    ax.set_yticks([])

    # 格式化 x 轴日期为月份缩写
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())  # 每个月设置一个刻度

    ax.set_title("GitHub Contributions", fontsize=16)
    plt.colorbar(scatter, label="Contributions")
    plt.tight_layout()

    # 保存图片
    plt.savefig("contributions.png")
    plt.close()


if __name__ == "__main__":
    username = "MingcanYang"  
    token = os.getenv("PAT_TOKEN")  # 从环境变量中获取 Token
    if not token:
        raise ValueError("PAT_TOKEN is not set. Please check your workflow environment.")
    weeks = get_contribution_data(username, token)
    generate_contribution_image(weeks)
