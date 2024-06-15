"""Helper class to connect to Dashboard API and obtain base types."""

import logging
from typing import Any
from typing import Dict
from typing import Generator
from typing import List
from typing import Optional

from engineai.sdk.dashboard.clients.activate_dashboard import ActivateDashboard
from engineai.sdk.internal.clients import APIClient
from engineai.sdk.internal.clients.exceptions import DashboardAPINoVersionFoundError

logger = logging.getLogger(__name__)
logging.getLogger("urllib3").propagate = False


class DashboardAPI(APIClient):
    """Dashboard API Connector and Types."""

    def publish_dashboard(self, dashboard: Dict[Any, Any]) -> Optional[Dict[Any, Any]]:
        """Publish a Dashboard."""
        content = self._request(
            query="""
                mutation PublishDashboard ($input: DashboardInput!) {
                    publishDashboard(input: $input) {
                        run
                        id
                        version
                        url
                        appId
                        warnings {
                            message
                        }
                    }
                }
            """,
            variables={"input": dashboard},
        )

        data = content.get("data", {}).get("publishDashboard", {})

        if data is None:
            return None

        return {
            "url_path": data.get("url"),
            "dashboard_id": data.get("id"),
            "version": data.get("version", None),
            "run": data.get("run", None),
            "app_id": data.get("appId"),
            "dashboard_slug": dashboard.get("slug", "").replace(" ", "-"),
        }

    def get_dashboard(
        self, dashboard_slug: str, app_id: Optional[str], version: Optional[str]
    ) -> None:
        """Get a dashboard."""
        return self._request(
            query="""query Dashboard($slug: String, $appId: String!, $version: String) {
                dashboard(slug: $slug, appId: $appId, version: $version) {
                    name
                }
            }""",
            variables={
                "slug": dashboard_slug,
                "appId": app_id,
                "version": version or "none",
            },
        )

    def get_dashboard_by_slug(
        self, dashboard_slug: str, version: str, run: str, app_id: Optional[str]
    ) -> Any:
        """Get a dashboard."""
        return (
            self._request(
                query="""
        query Query($slug: String!, $appId: String!, $version: String, $run: String) {
            dashboard(slug: $slug, appId: $appId, version: $version, run: $run) {
                id
            }
        }""",
                variables={
                    "slug": dashboard_slug,
                    "appId": app_id,
                    "version": version,
                    "run": run,
                },
            )
            .get("data", {})
            .get("dashboard", {})
            .get("id", "")
        )

    def list_my_apps(self) -> List:
        """List user's apps."""
        return (
            self._request(
                query="""
                query Apps {
                    myApps {
                        apps {
                            appId
                        }
                    }
                }"""
            )
            .get("data", {})
            .get("myApps", {})
            .get("apps", [])
        )

    def list_my_dashboards(self, app_id: str) -> List:
        """List user's dashboards."""
        return (
            self._request(
                query="""
                query Apps($appId: String!) {
                    app(appId: $appId) {
                        dashboards {
                            name
                            slug
                        }
                    }
                }""",
                variables={"appId": app_id},
            )
            .get("data", {})
            .get("app", {})
            .get("dashboards", [])
        )

    def list_dashboard_versions(self, app_id: str, dashboard_slug: str) -> Generator:
        """List dashboard versions."""
        dashboard_versions = self._get_dashboard_versions(app_id, dashboard_slug)
        yield from dashboard_versions

    def list_dashboard_runs(
        self, app_id: str, dashboard_slug: str, version: str
    ) -> Generator:
        """List dashboard version runs."""
        dashboard_versions = self._get_dashboard_versions(app_id, dashboard_slug)
        for dashboard_version in dashboard_versions:
            if dashboard_version.get("version") == version:
                yield from dashboard_version.get("runs", [])
                break

    def activate_dashboard(self, activate_dashboard: ActivateDashboard) -> None:
        """Activate a dashboard."""
        activate_dashboard_spec = activate_dashboard.build()

        return self._request(
            query="""
                mutation ActivateDashboard($input: ActivateDashboardInput!) {
                    activateDashboard(input: $input)
                }""",
            variables={"input": activate_dashboard_spec},
        )

    def activate_dashboard_by_slug(
        self,
        app_id: str,
        slug: str,
        version: str,
        run: str,
        activate_version: bool = True,
    ) -> None:
        """Activate a dashboard."""
        dashboard_id = self.get_dashboard_by_slug(slug, version, run, app_id)
        activate_dashboard_spec = (
            ActivateDashboard(
                dashboard_id=dashboard_id,
                version=version,
                run=run,
                activate_version=activate_version,
            )
            .build()
            .to_dict()
        )

        return self._request(
            query="""
                mutation ActivateDashboard($input: ActivateDashboardInput!) {
                    activateDashboard(input: $input)
                }""",
            variables={"input": activate_dashboard_spec},
        )

    def _get_dashboard_versions(self, app_id: str, dashboard_slug: str) -> List:
        dashboard_versions = (
            self._request(
                query="""
                query DashboardVersions($appId: String!, $slug: String!) {
                    dashboardVersions(appId: $appId, slug: $slug) {
                        version
                        active
                        runs {
                            slug
                            active
                        }
                    }
                }""",
                variables={"appId": app_id, "slug": dashboard_slug},
            )
            .get("data", {})
            .get("dashboardVersions", [])
        )
        return dashboard_versions or []

    def _get_api_version(self) -> str:
        content = self._request(query="query Version {version { tag } }")

        if not self._version_content_valid(content):
            raise DashboardAPINoVersionFoundError()

        return str(content.get("data").get("version").get("tag").replace("v", ""))

    @staticmethod
    def _version_content_valid(content: Dict[str, Any]) -> bool:
        return (
            "data" in content
            and "version" in content.get("data", {})
            and "tag" in content.get("data", {}).get("version", {})
        )

    # Account Mutation
    def update_account(self, account_name: str, new_account_name: str) -> Any:
        """Update Account."""
        return self._request(
            query="""
                mutation updateAccount($input: UpdateAccountInput!) {
                updateAccount(input: $input) {
                    account {
                    slug
                    }
                }
                }
                """,
            variables={"input": {"slug": account_name, "newSlug": new_account_name}},
        )

    def create_account(self, account_name: str) -> Any:
        """Create Account."""
        return self._request(
            query="""
                mutation createAccount($input: CreateAccountInput!) {
                createAccount(input: $input) {
                    account {
                    slug
                    }
                }
                }""",
            variables={"input": {"slug": account_name}},
        )

    def delete_account(self, account_name: str) -> Any:
        """Delete Account."""
        return self._request(
            query="""
                mutation deleteAccount($input: DeleteAccountInput!) {
                deleteAccount(input: $input)
                }
                """,
            variables={"input": {"slug": account_name}},
        )

    def list_account(self) -> List:
        """List all Accounts."""
        return (
            (
                self._request(
                    query="""
                query ListAccounts {
                    accounts
                    {
                    id
                    slug
                    }
                }"""
                )
            )
            .get("data", {})
            .get("accounts", [])
        )

    def add_account_member(self, account_name: str, email: str, role: str) -> List:
        """Add memeber to account."""
        return self._request(
            query="""
                    mutation addAccountMember($input: AddAccountMemberInput!) {
                        addAccountMember(input: $input) {
                        account {
                            slug
                        }
                        }
                    }""",
            variables={
                "input": {"accountSlug": account_name, "userEmail": email, "role": role}
            },
        ).get("data", {})

    def update_account_member(self, account_name: str, email: str, role: str) -> List:
        """Update account member."""
        return self._request(
            query="""
                    mutation updateAccountMember($input: UpdateAccountMemberInput!) {
                    updateAccountMember(input: $input) {
                        account {
                            slug
                            members {
                                user {
                                    email
                                }
                                role
                            }
                        }
                    }
                    }""",
            variables={
                "input": {"accountSlug": account_name, "userEmail": email, "role": role}
            },
        ).get("data", {})

    def remove_account_member(self, account_name: str, email: str) -> List:
        """Remove account member."""
        return self._request(
            query="""
                    mutation removeAccountMember($input: RemoveAccountMemberInput!) {
                        removeAccountMember(input: $input) {
                            account {
                                slug
                            }
                        }
                    }""",
            variables={"input": {"accountSlug": account_name, "userEmail": email}},
        ).get("data", {})

    def list_account_member(self, account_name: str) -> List:
        """List all accounts members."""
        return (
            (
                self._request(
                    query="""
                        query ListAccountsMember ($slug: String!) {
                            account (slug: $slug){
                                slug
                                members {
                                    user {
                                        email
                                    }
                                    role
                                }
                            }
                        }""",
                    variables={"slug": account_name},
                )
            )
            .get("data", {})
            .get("account", {})
        )

    def transfer_account(self, account_name: str, email: str) -> List:
        """Transfer account to another user."""
        return self._request(
            query="""
                    mutation transferAccount($input: TransferAccountInput!) {
                    transferAccount(input: $input) {
                        account {
                            slug
                            members {
                                user {
                                    email
                                }
                                role
                            }
                        }
                    }
                    }""",
            variables={"input": {"accountSlug": account_name, "userEmail": email}},
        ).get("data", {})
