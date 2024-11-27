import requests
import matplotlib.pyplot as plt
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
    ax.set_xticks([dates[0] + datetime.timedelta(days=7 * i) for i in range(len(dates) // 7)])
    ax.set_xticklabels([date.strftime("%b") for date in ax.get_xticks()])
    ax.set_title("GitHub Contributions", fontsize=16)
    plt.colorbar(scatter, label="Contributions")
    plt.tight_layout()

    
    plt.savefig("contributions.png")
    plt.close()

if __name__ == "__main__":
    username = "MingcanYang"  
    token = os.getenv("GITHUB_TOKEN")  
    weeks = get_contribution_data(username, token)
    generate_contribution_image(weeks)
