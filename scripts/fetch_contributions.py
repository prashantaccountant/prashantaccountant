"""Fetch the last year of GitHub contributions into data/contributions.json.

Env:
  GH_USER   GitHub username (required)
  GH_TOKEN  token for the GraphQL API (GITHUB_TOKEN works for public data;
            a personal access token also counts private contributions)
"""
import json
import os
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def main():
    user = os.environ.get("GH_USER")
    token = os.environ.get("GH_TOKEN")
    if not user or not token:
        sys.exit("Set GH_USER and GH_TOKEN")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [
        {"date": d["date"], "count": d["contributionCount"]}
        for w in cal["weeks"]
        for d in w["contributionDays"]
    ]
    os.makedirs("data", exist_ok=True)
    with open("data/contributions.json", "w") as f:
        json.dump({"user": user, "total": cal["totalContributions"], "days": days}, f)
    print(f"Saved {len(days)} days, {cal['totalContributions']} contributions")


if __name__ == "__main__":
    main()
