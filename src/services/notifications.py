"""
    Github notifications services.
"""

from datetime import datetime, timezone
from github import Github, Auth
from github.PaginatedList import PaginatedList
from github.Notification import Notification


def get_notifications_by_access_token(
    access_token: str, since: datetime | None
) -> PaginatedList[Notification]:
    auth = Auth.Token(access_token)
    gh = Github(auth=auth)

    if since is not None:
        notificatons = gh.get_user().get_notifications(since=since)
    else:
        notificatons = gh.get_user().get_notifications()
        gh.get_user().mark_notifications_as_read
    return notificatons


def mark_notifications_as_read(access_token: str) -> None:
    auth = Auth.Token(access_token)
    gh = Github(auth=auth)
    gh.get_user().mark_notifications_as_read()


def updated_at_to_formatted_timedelta(updated_at: datetime) -> str:
    timedelta = datetime.now(timezone.utc) - updated_at
    days = int(timedelta.total_seconds()//86400)
    if days % 10 == 1 and days % 100 != 11:
        return f"{days} день назад"
    elif 1 < days % 10 < 5 and days % 100 - days % 10 != 10:
        return f"{days} дня назад"
    elif days > 0:
        return f"{days} дней назад"

    hours = int(timedelta.total_seconds()//3600)
    if hours % 10 == 1 and hours % 100 != 11:
        return f"{hours} час назад"
    elif 1 < hours % 10 < 5 and hours % 100 - hours % 10 != 10:
        return f"{hours} часа назад"
    elif hours > 0:
        return f"{hours} часов назад"

    minutes = int(timedelta.total_seconds() % 3600 // 60)
    if minutes % 10 == 1 and minutes % 100 != 11:
        return f"{minutes} минута назад"
    elif 1 < minutes % 10 < 5 and minutes % 100 - minutes % 10 != 10:
        return f"{minutes} минуты назад"
    return f"{minutes} минут назад"
