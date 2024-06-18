from datetime import datetime

import humanize

from models import User, IssueWithUsersAndTeams, GithubInfo


def issue_to_tabulate(issue: IssueWithUsersAndTeams, github_info: GithubInfo) -> list[str]:
    title = f"[DRAFT] {issue.title}" if issue.draft else issue.title

    creator_with_url = format_url(str(issue.creator), issue.creator.html_url)
    creator = make_bold(str(creator_with_url)) if issue.creator in github_info.team else str(creator_with_url)
    repo_url = issue.html_url.split("/pull")[0]

    return [
        format_url(title, issue.html_url),
        format_url(issue.repo.name, repo_url),
        humanize_date(issue.updated_at),
        creator,
        sort_assigned_team_user(issue.assigned_team_user, github_info.user),
        humanize_date(issue.created_at),
    ]


def make_bold(text: str) -> str:
    return f"[bold]{text}[/bold]"


def sort_assigned_team_user(assigned_team_user: set[User], user: User) -> str:
    str_users = [format_url(u.login, u.html_url) for u in assigned_team_user if u != user]

    if user in assigned_team_user:
        str_user = make_bold(format_url(user.login, user.html_url))
        str_users = [str_user] + str_users

    return ", ".join(str_users)


def humanize_date(date: datetime) -> str:
    now = datetime.now()
    diff = now - date
    return humanize.naturaltime(now - diff)


def format_url(title: str, url: str) -> str:
    return f"[link={url}]{title}[/link]"

