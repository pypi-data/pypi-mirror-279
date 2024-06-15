from asyncio import Future
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from rich.table import Table
import click
import requests

from models import GithubInfo, Issue, IssueWithUsersAndTeams, User
from utils import issue_to_tabulate

API_URL = "https://api.github.com/"


def get_headers(token: str) -> dict:
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def retrieve_github_info(user: str, org: str, team_name: str, token: str) -> GithubInfo:
    issues_url = f"{API_URL}/orgs/{org}/teams/{team_name}/members"
    response = requests.get(issues_url, headers=get_headers(token))
    team_users = {User(login=team_user["login"]) for team_user in response.json()}
    return GithubInfo(user=User(login=user), org=org, team=team_users, token=token)


def get_issues(github_info: GithubInfo) -> list[Issue]:
    issues_url = f"{API_URL}/search/issues?q=is:pr+is:open+review-requested:{github_info.user.login}"
    response = requests.get(issues_url, headers=get_headers(github_info.token))
    prs = response.json()["items"]
    return [Issue.from_dict(pr) for pr in prs]


def get_reviewers(issue: Issue, github_info: GithubInfo) -> IssueWithUsersAndTeams:
    reviewers_url = f"{API_URL}/repos/{github_info.org}/{issue.repo.name}/pulls/{issue.number}/requested_reviewers"
    response = requests.get(reviewers_url, headers=get_headers(github_info.token))
    reviewers = response.json()
    users = {User.from_dict(user) for user in reviewers["users"]}

    return IssueWithUsersAndTeams.from_issue(
        issue, users, github_info.user, github_info.team
    )

def retrieve_issues_with_users_and_teams(github_info: GithubInfo, issues: list[Issue]) -> list[IssueWithUsersAndTeams]:
    _futures: list[Future[IssueWithUsersAndTeams]] = []
    with ThreadPoolExecutor() as executor:
        for issue in issues:
            _futures.append(executor.submit(get_reviewers, issue, github_info))
    futures.wait(_futures)
    issues_with_users_and_teams = [future.result() for future in _futures]
    return issues_with_users_and_teams


def pretty_print_issues_with_users_and_teams(
    issues: list[IssueWithUsersAndTeams], github_info: GithubInfo, console: Console, recent_first: bool
):
    sort_lambda = lambda x: (not x.user_in_users, x.updated_at if not recent_first else -x.updated_at.timestamp())
    sorted_issues = sorted(issues, key=sort_lambda)

    tabulate_ready_issues = [
        issue_to_tabulate(issue, github_info.user, github_info.team) for issue in sorted_issues
    ]
    if index := [i for i, issue in enumerate(sorted_issues) if not issue.user_in_users]:
        tabulate_ready_issues.insert(index[0], ["", "", "", "", ""])

    table = Table(title="Opened issues")

    table.add_column("Title", justify="center", style="cyan")
    table.add_column("Updated", justify="center", style="green")
    table.add_column("Creator", justify="center", style="magenta")
    table.add_column("Reviewer in team", justify="center", style="magenta")
    table.add_column("Created", justify="center", style="green")

    for tabulate_ready_issue in tabulate_ready_issues:
        table.add_row(*tabulate_ready_issue)

    console.print(table)


@click.command()
@click.option("--user", help=f"User name from github", required=True)
@click.option("--org", help=f"Org name from github", required=True)
@click.option("--token", help=f"Token from github", required=True)
@click.option("--team", help=f"Team name from github", required=True)
@click.option("--show-draft", is_flag=True, help=f"Show draft PRs")
@click.option("--recent-first", is_flag=True, help=f"Show recent PRs on top of the list (instead of oldest)")
@click.version_option(package_name="github-review-requested")
def github_review_requested(user: str, org: str, token: str, team: str, show_draft: bool, recent_first: bool):
    console = Console()
    with console.status("[bold green] Fetching issues..."):
        github_info = retrieve_github_info(user, org, team, token)
        issues = get_issues(github_info)
        issues_with_users_and_teams = retrieve_issues_with_users_and_teams(github_info, issues)

    if not show_draft:
        issues_with_users_and_teams = [
            issue for issue in issues_with_users_and_teams if not issue.draft
        ]

    pretty_print_issues_with_users_and_teams(issues_with_users_and_teams, github_info, console, recent_first)


if __name__ == "__main__":
    github_review_requested()