import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

    ax.set_yticks([])

    # 使用 matplotlib.dates 处理 x 轴日期
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    ax.set_title("GitHub Contributions", fontsize=16)
    plt.colorbar(scatter, label="Contributions")
    plt.tight_layout()

    plt.savefig("contributions.png")
    plt.close()


if __name__ == "__main__":
    username = "MingcanYang"  
    token = os.getenv("PAT_TOKEN")
    if not token:
        raise ValueError("PAT_TOKEN is not set. Please check your workflow environment.")
    weeks = get_contribution_data(username, token)
    generate_contribution_image(weeks)
