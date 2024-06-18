"""Scanner for PR force-pushed dangling-commits"""

import requests
from rich.console import Console

from dangling_finder.exceptions import GitHubRepoError

err_console = Console(stderr=True)


class _GraphQL:
    """Class for graphQL queries of force-pushed PRs"""

    def __init__(self, owner, repo, github_token):
        self._github_token = github_token
        self._repo = repo
        self._owner = owner
        self._rest_headers = {
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {self._github_token}",
            "Accept": "application/vnd.github+json",
        }

    def check_repository(self):
        url_api = f"https://api.github.com/repos/{self._owner}/{self._repo}"
        url_repo = f"https://github.com/{self._owner}/{self._repo}"
        err_console.print(f"Loading dangling commits on GitHub: {url_repo}")
        r = requests.get(url_api, headers=self._rest_headers, timeout=10)
        if r.status_code != 200:
            raise GitHubRepoError(
                f"Could not connect to the following repo: {url_repo}"
            )
        err_console.print("✅ GitHub repository found")

    def get_pull_request_highest_number(self):
        url = (
            f"https://api.github.com/repos/{self._owner}/{self._repo}/pulls"
            "?state=all"
        )
        resp = requests.get(url, headers=self._rest_headers, timeout=10)
        body = resp.json()
        if len(body) == 0:
            return 0
        return body[0]["number"]

    def extract_from_single_graphql_response(self, result):
        found_dangling_heads = []
        found_closed_not_merged_prs = []
        has_next_page = result["data"]["repository"]["pullRequests"][
            "pageInfo"
        ]["hasNextPage"]
        new_cursor = result["data"]["repository"]["pullRequests"]["pageInfo"][
            "endCursor"
        ]
        cost_add = result["data"]["rateLimit"]["cost"]

        result_data = result["data"]["repository"]["pullRequests"]["nodes"]
        # 1. extract heads of PR not merged and closed
        for pull_request in result_data:
            if (pull_request["closed"] is True) and (
                pull_request["merged"] is False
            ):
                found_closed_not_merged_prs.append(pull_request["id"])
            forced_pushed_events = pull_request["timelineItems"]["nodes"]
            # 2. extract heads from force-pushed events
            if len(forced_pushed_events) > 0:
                for dangling_head in forced_pushed_events:
                    before_commit = dangling_head["beforeCommit"]
                    # see issue 6
                    if before_commit is not None:
                        commit_author = before_commit["author"]
                        commit_head = {
                            "commitUrl": before_commit["commitUrl"],
                            "commitSHA": before_commit["commitUrl"].split("/")[
                                -1
                            ],
                            "author": {
                                "name": commit_author["name"],
                                "email": commit_author["email"],
                            },
                            "date": before_commit["authoredDate"],
                            "type": {
                                "name": "ForcePushed PR",
                                "PR": pull_request["url"],
                            },
                        }
                        found_dangling_heads += [commit_head]
        return (
            has_next_page,
            new_cursor,
            cost_add,
            found_dangling_heads,
            found_closed_not_merged_prs,
        )

    def extract_closed_pr_response(self, result):
        closed_pr_head_commits = []
        cost_add = result["data"]["rateLimit"]["cost"]
        result_data = result["data"]["nodes"]
        for node in result_data:
            # if PR force-pushed to begin (no commit in PR)
            # cf. https://github.com/akeneo/pim-community-dev/pull/2025
            if len(node["commits"]["nodes"]) > 0:
                pull_request = node
                commit = node["commits"]["nodes"][0]["commit"]
                commit_author = commit["author"]
                commit_result = {
                    "commitUrl": commit["commitUrl"],
                    "commitSHA": commit["commitUrl"].split("/")[-1],
                    "author": {
                        "name": commit_author["name"],
                        "email": commit_author["email"],
                    },
                    "date": commit["authoredDate"],
                    "type": {
                        "name": "Closed PR",
                        "PR": pull_request["url"],
                    },
                }
                closed_pr_head_commits.append(commit_result)
        return cost_add, closed_pr_head_commits

    def execute_closed_pr_queries(self, pr_list, previous_rate_limit):
        if len(pr_list) == 0:
            return [], previous_rate_limit
        dangling_heads = []
        total_cost = 0
        query = """
        query ($ids: [ID!]!) {
        rateLimit {
            resetAt
            cost
            remaining
        }
        nodes(ids: $ids) {
            ... on PullRequest {
            url
            commits(last: 1) {
                nodes {
                commit {
                    authoredDate
                    author { name, email }
                    commitUrl
                }
                }
            }
            }
        }
        }
        """
        nb_queries = len(pr_list) // 100 + (len(pr_list) % 100 > 0)
        for i in range(nb_queries):
            variables = {"ids": pr_list[i * 100 : (i + 1) * 100]}
            request = requests.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": variables},
                headers={
                    "Authorization": f"Bearer {self._github_token}",
                    "X-Github-Next-Global-ID": "1",
                },
                timeout=10,
            )
            if request.status_code == 200:
                result = request.json()
                cost_add, found_dangling_closed_commits = (
                    self.extract_closed_pr_response(result)
                )
                dangling_heads += found_dangling_closed_commits
                total_cost += cost_add
            else:
                raise GitHubRepoError(
                    f"""Query failed to run, code: {request.status_code}.
                    Response body:\n{request.text}
                    Response headers:\n{request.headers}"""
                )
        remaining_rate_limit = result["data"]["rateLimit"]
        remaining_rate_limit["total"] = (
            total_cost + previous_rate_limit["total"]
        )
        return dangling_heads, remaining_rate_limit

    def execute_force_pushed_queries(self):
        i = 0
        end_cursor = ""
        dangling_heads = []
        closed_prs = []
        total_cost = 0
        total_time = 0
        query = """
        query ($owner: String!, $repo: String!, $endCursor: String!) {
        rateLimit {
            resetAt
            cost
            remaining
        }
        repository(name: $repo, owner: $owner ) {
            pullRequests(first: 100, after: $endCursor) {
            pageInfo {
                hasNextPage
                endCursor
            }
            nodes {
                ... on PullRequest {
                id
                url
                number
                closed
                merged
                timelineItems(first: 100, itemTypes: \
        [HEAD_REF_FORCE_PUSHED_EVENT]) {
                    nodes {
                    ... on HeadRefForcePushedEvent {
                        beforeCommit {
                        authoredDate
                        author { name, email }
                        commitUrl
                        }
                    }
                    }
                }
                }
            }
            }
        }
        }
        """
        while True:
            current_query = query
            variables = {
                "owner": self._owner,
                "repo": self._repo,
                "endCursor": end_cursor,
            }
            if total_cost == 0:
                current_query = current_query.replace(
                    ", $endCursor: String!", ""
                )
                current_query = current_query.replace(", after: $endCursor", "")
                variables.pop("endCursor")
            request = requests.post(
                "https://api.github.com/graphql",
                json={"query": current_query, "variables": variables},
                headers={
                    "Authorization": f"Bearer {self._github_token}",
                    "X-Github-Next-Global-ID": "1",
                },
                timeout=10,
            )
            i += 1
            if request.status_code == 200:
                result = request.json()
                (
                    has_next_page,
                    new_cursor,
                    cost_add,
                    found_dangling_heads,
                    found_closed_pr_heads,
                ) = self.extract_from_single_graphql_response(result)
                total_cost += cost_add
                total_time += request.elapsed.total_seconds()
                dangling_heads += found_dangling_heads
                closed_prs += found_closed_pr_heads
                if has_next_page:
                    end_cursor = new_cursor
                else:
                    break
            else:
                raise GitHubRepoError(
                    f"""Query failed to run, code: {request.status_code}.
                    Response body:\n{request.text}
                    Response headers:\n{request.headers}"""
                )
        remaining_rate_limit = result["data"]["rateLimit"]
        remaining_rate_limit["total"] = total_cost
        remaining_rate_limit["total_time"] = total_time
        return (
            dangling_heads,
            remaining_rate_limit,
            closed_prs,
        )
