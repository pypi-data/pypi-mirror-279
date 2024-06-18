# Copyright 2023 Cognite AS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from importlib import resources
from pathlib import Path
from time import sleep
from typing import cast

from cognite.client import CogniteClient
from cognite.client.data_classes.capabilities import (
    FunctionsAcl,
    UserProfilesAcl,
)
from cognite.client.data_classes.iam import Group, GroupList, TokenInspection
from cognite.client.exceptions import CogniteAPIError
from rich import print
from rich.markup import escape
from rich.prompt import Confirm, Prompt
from rich.table import Table

from cognite_toolkit._cdf_tk.constants import COGNITE_MODULES
from cognite_toolkit._cdf_tk.exceptions import (
    AuthorizationError,
    ResourceCreationError,
    ResourceDeleteError,
    ResourceRetrievalError,
    ToolkitFileNotFoundError,
    ToolkitInvalidSettingsError,
)
from cognite_toolkit._cdf_tk.tk_warnings import (
    HighSeverityWarning,
    LowSeverityWarning,
    MediumSeverityWarning,
    MissingCapabilityWarning,
)
from cognite_toolkit._cdf_tk.utils import AuthVariables, CDFToolConfig

from ._base import ToolkitCommand


class AuthCommand(ToolkitCommand):
    def execute(
        self,
        ToolGlobals: CDFToolConfig,
        dry_run: bool,
        interactive: bool,
        group_file: str | None,
        update_group: int,
        create_group: str | None,
        verbose: bool,
    ) -> None:
        # TODO: Check if groupsAcl.UPDATE does nothing?
        if create_group is not None and update_group != 0:
            raise ToolkitInvalidSettingsError("--create-group and --update-group are mutually exclusive.")

        if group_file is None:
            template_dir = cast(Path, resources.files("cognite_toolkit"))
            group_path = template_dir.joinpath(
                Path(f"./{COGNITE_MODULES}/common/cdf_auth_readwrite_all/auth/admin.readwrite.group.yaml")
            )
        else:
            group_path = Path(group_file)
        self.check_auth(
            ToolGlobals,
            group_file=group_path,
            update_group=update_group,
            create_group=create_group,
            interactive=interactive,
            dry_run=dry_run,
            verbose=verbose,
        )

    def check_auth(
        self,
        ToolGlobals: CDFToolConfig,
        group_file: Path,
        update_group: int = 0,
        create_group: str | None = None,
        interactive: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        auth_vars = self.initialize_client(ToolGlobals, interactive, verbose)
        if auth_vars.project is None:
            raise AuthorizationError("CDF_PROJECT is not set.")
        cdf_project = auth_vars.project
        token_inspection = self.check_has_any_access(ToolGlobals)

        self.check_has_project_access(token_inspection, cdf_project)

        print(f"[italic]Focusing on current project {cdf_project} only from here on.[/]")

        self.check_has_group_access(ToolGlobals)

        self.check_identity_provider(ToolGlobals, cdf_project)

        try:
            groups = ToolGlobals.client.iam.groups.list()
        except CogniteAPIError as e:
            raise AuthorizationError(f"Unable to retrieve CDF groups.\n{e}")

        read_write, matched_group_id = self.check_group_membership(groups, group_file, update_group)

        self.check_has_toolkit_required_capabilities(
            ToolGlobals.client, token_inspection, read_write, cdf_project, group_file.name
        )
        print("---------------------")
        self.check_capabilities_against_groups(ToolGlobals, token_inspection, auth_vars, groups, update_group)

        self.update_group(
            ToolGlobals,
            groups,
            group_file,
            read_write,
            matched_group_id,
            update_group,
            create_group,
            interactive,
            dry_run,
        )
        self.check_function_service_status(ToolGlobals, token_inspection, cdf_project, dry_run)

    def initialize_client(self, ToolGlobals: CDFToolConfig, interactive: bool, verbose: bool) -> AuthVariables:
        print("[bold]Checking current service principal/application and environment configurations...[/]")
        auth_vars = AuthVariables.from_env()
        if interactive:
            result = auth_vars.from_interactive_with_validation(verbose)
        else:
            result = auth_vars.validate(verbose)
        if result.messages:
            print("\n".join(result.messages))
        print("  [bold green]OK[/]")
        ToolGlobals.initialize_from_auth_variables(auth_vars)
        return auth_vars

    def check_has_any_access(self, ToolGlobals: CDFToolConfig) -> TokenInspection:
        print("Checking basic project configuration...")
        try:
            # Using the token/inspect endpoint to check if the client has access to the project.
            # The response also includes access rights, which can be used to check if the client has the
            # correct access for what you want to do.
            token_inspection = ToolGlobals.client.iam.token.inspect()
            if token_inspection is None or len(token_inspection.capabilities) == 0:
                raise AuthorizationError(
                    "Valid authentication token, but it does not give any access rights."
                    " Check credentials (CDF_CLIENT_ID/CDF_CLIENT_SECRET or CDF_TOKEN)."
                )
            print("  [bold green]OK[/]")
        except Exception:
            raise AuthorizationError(
                "Not a valid authentication token. Check credentials (CDF_CLIENT_ID/CDF_CLIENT_SECRET or CDF_TOKEN)."
            )
        return token_inspection

    def check_has_project_access(self, token_inspection: TokenInspection, cdf_project: str) -> None:
        print("Checking projects that the service principal/application has access to...")
        if len(token_inspection.projects) == 0:
            raise AuthorizationError(
                "The service principal/application configured for this client does not have access to any projects."
            )
        print("\n".join(f"  - {p.url_name}" for p in token_inspection.projects))
        if cdf_project not in {p.url_name for p in token_inspection.projects}:
            raise AuthorizationError(
                f"The service principal/application configured for this client does not have access to the CDF_PROJECT={cdf_project!r}."
            )

    def check_has_group_access(self, ToolGlobals: CDFToolConfig) -> None:
        # Todo rewrite to use the token inspection instead.
        print(
            "Checking basic project and group manipulation access rights "
            "(projectsAcl: LIST, READ and groupsAcl: LIST, READ, CREATE, UPDATE, DELETE)..."
        )
        try:
            ToolGlobals.verify_client(
                capabilities={
                    "projectsAcl": [
                        "LIST",
                        "READ",
                    ],
                    "groupsAcl": ["LIST", "READ", "CREATE", "UPDATE", "DELETE"],
                }
            )
            print("  [bold green]OK[/]")
        except Exception:
            self.warn(
                HighSeverityWarning(
                    "The service principal/application configured for this client "
                    "does not have the basic group write access rights."
                )
            )
            print("Checking basic group read access rights (projectsAcl: LIST, READ and groupsAcl: LIST, READ)...")
            try:
                ToolGlobals.verify_client(
                    capabilities={
                        "projectsAcl": ["LIST", "READ"],
                        "groupsAcl": ["LIST", "READ"],
                    }
                )
                print("  [bold green]OK[/] - can continue with checks.")
            except Exception:
                raise AuthorizationError(
                    "Unable to continue, the service principal/application configured for this client does not"
                    " have the basic read group access rights."
                )

    def check_identity_provider(self, ToolGlobals: CDFToolConfig, cdf_project: str) -> None:
        print("Checking identity provider settings...")
        project_info = ToolGlobals.client.get(f"/api/v1/projects/{cdf_project}").json()
        oidc = project_info.get("oidcConfiguration", {})
        if "https://login.windows.net" in oidc.get("tokenUrl"):
            tenant_id = oidc.get("tokenUrl").split("/")[-3]
            print(f"  [bold green]OK[/]: Microsoft Entra ID (aka ActiveDirectory) with tenant id ({tenant_id}).")
        elif "auth0.com" in oidc.get("tokenUrl"):
            tenant_id = oidc.get("tokenUrl").split("/")[2].split(".")[0]
            print(f"  [bold green]OK[/] - Auth0 with tenant id ({tenant_id}).")
        else:
            self.warn(MediumSeverityWarning(f"Unknown identity provider {oidc.get('tokenUrl')}"))
        access_claims = [c.get("claimName") for c in oidc.get("accessClaims", {})]
        print(
            f"  Matching on CDF group sourceIds will be done on any of these claims from the identity provider: {access_claims}"
        )

    def check_group_membership(self, groups: GroupList, group_file: Path, update_group: int) -> tuple[Group, int]:
        print("Checking CDF group memberships for the current client configured...")
        if group_file.exists():
            file_text = group_file.read_text()
        else:
            raise ToolkitFileNotFoundError(f"Group config file does not exist: {group_file.as_posix()}")
        read_write = Group.load(file_text)
        tbl = Table(title="CDF Group ids, Names, and Source Ids")
        tbl.add_column("Id", justify="left")
        tbl.add_column("Name", justify="left")
        tbl.add_column("Source Id", justify="left")
        matched_group_source_id = None
        matched_group_id = 0
        for g in groups:
            if len(groups) > 1 and g.name == read_write.name:
                matched_group_source_id = g.source_id
                matched_group_id = g.id
                tbl.add_row(str(g.id), "[bold]" + g.name + "[/]", g.source_id)
            else:
                tbl.add_row(str(g.id), g.name, g.source_id)
        multiple_groups_with_source_id = 0
        for g in groups:
            if g.source_id == matched_group_source_id:
                multiple_groups_with_source_id += 1
        print(tbl)
        if len(groups) > 1:
            self.warn(
                LowSeverityWarning(
                    "This service principal/application gets its access rights from more than one CDF group."
                )
            )
            print(
                "           This is not recommended. The group matching the group config file is marked in bold above if it is present."
            )
            if update_group == 1:
                raise AuthorizationError(
                    "You have specified --update-group=1.\n"
                    "         With multiple groups available, you must use the --update_group=<full-group-i> "
                    "option to specify which group to update."
                )
        else:
            print("  [bold green]OK[/] - Only one group is used for this service principal/application.")
        print("---------------------")
        if matched_group_source_id is not None:
            print("[bold green]RECOMMENDATION[/]:")
            print(f"  You have {multiple_groups_with_source_id} groups with source id {matched_group_source_id},")
            print(
                f"  which is the same source id as the [italic]{escape(read_write.name)}[/] group in the group config file."
            )
            print(
                "  It is recommended that this admin (CI/CD) application/service principal only is member of one group in the identity provider."
            )
            print(
                "  This group's id should be configured as the [italic]readwrite_source_id[/] for the common/cdf_auth_readwrite_all module."
            )
        return read_write, matched_group_id

    def check_has_toolkit_required_capabilities(
        self,
        client: CogniteClient,
        token_inspection: TokenInspection,
        read_write: Group,
        cdf_project: str,
        group_file_name: str,
    ) -> None:
        print(f"\nChecking CDF groups access right against capabilities in {group_file_name} ...")

        diff = client.iam.compare_capabilities(
            token_inspection.capabilities,
            read_write.capabilities or [],
            project=cdf_project,
        )
        if len(diff) > 0:
            diff_list: list[str] = []
            for d in diff:
                diff_list.append(str(d))
            for s in sorted(diff_list):
                self.warn(MissingCapabilityWarning(str(s)))
        else:
            print("  [bold green]OK[/] - All capabilities are present in the CDF project.")

    def check_capabilities_against_groups(
        self,
        ToolGlobals: CDFToolConfig,
        token_inspection: TokenInspection,
        auth_vars: AuthVariables,
        groups: GroupList,
        update_group: int,
    ) -> None:
        # Flatten out into a list of acls in the existing project
        existing_cap_list = [c.capability for c in token_inspection.capabilities]
        if len(groups) > 1 and update_group > 1:
            print(f"Checking group config file against capabilities only from the group {update_group}...")
            for g in groups:
                if g.id == update_group:
                    existing_cap_list = g.capabilities or []
                    break
        else:
            if len(groups) > 1:
                print("Checking group config file against capabilities across [bold]ALL[/] groups...")
            else:
                print("Checking group config file against capabilities in the group...")

        loosing = ToolGlobals.client.iam.compare_capabilities(
            existing_cap_list,
            token_inspection.capabilities,
            project=auth_vars.project,
        )
        loosing = [l for l in loosing if type(l) is not UserProfilesAcl]  # noqa: E741
        if len(loosing) > 0:
            for d in loosing:
                if len(groups) > 1:
                    self.warn(
                        LowSeverityWarning(
                            f"The capability {d} may be lost if\n"
                            "           switching to relying on only one group based on "
                            "group config file for access."
                        )
                    )
                else:
                    self.warn(
                        LowSeverityWarning(
                            f"The capability {d} will be removed in the project if overwritten " "by group config file."
                        )
                    )
        else:
            print(
                "  [bold green]OK[/] - All capabilities from the CDF project are also present in the group config file."
            )
        print("---------------------")

    def update_group(
        self,
        ToolGlobals: CDFToolConfig,
        groups: GroupList,
        group_file: Path,
        read_write: Group,
        matched_group_id: int,
        update_group: int,
        create_group: str | None,
        interactive: bool,
        dry_run: bool,
    ) -> None:
        if interactive and matched_group_id != 0:
            push_group = Confirm.ask(
                f"Do you want to update the group with id {matched_group_id} and name {read_write.name} with the capabilities from {group_file.as_posix()} ?",
                choices=["y", "n"],
            )
            if push_group:
                update_group = matched_group_id
        elif interactive:
            push_group = Confirm.ask(
                "Do you want to create a new group with the capabilities from the group config file ?",
                choices=["y", "n"],
            )
            if push_group:
                create_group = Prompt.ask(
                    "What is the source id for the new group (typically a group id in the identity provider)? "
                )
        if len(groups) == 1 and update_group == 1:
            update_group = groups[0].id
        elif not interactive and matched_group_id != 0 and update_group == 1:
            update_group = matched_group_id
        if update_group > 1 or create_group is not None:
            if update_group > 0:
                print(f"Updating group {update_group}...")
                for g in groups:
                    if g.id == update_group:
                        group = g
                        break
                if group is None:
                    raise ResourceRetrievalError(f"Unable to find --group-id={update_group} in CDF.")
                read_write.name = group.name
                read_write.source_id = group.source_id
                read_write.metadata = group.metadata
            else:
                print(f"Creating new group based on {group_file.as_posix()}...")
                read_write.source_id = create_group
            try:
                if not dry_run:
                    new = ToolGlobals.client.iam.groups.create(read_write)
                    print(
                        f"  [bold green]OK[/] - Created new group {new.id} with {len(read_write.capabilities or [])} capabilities."
                    )
                    # Need to reinitialize the client to update the token with the new capabilities
                    # In addition sleep for a second to allow the IAM service to update the group
                    sleep(1.0)
                    ToolGlobals.reinitialize_client()
                else:
                    print(
                        f"  [bold green]OK[/] - Would have created new group with {len(read_write.capabilities or [])} capabilities."
                    )
            except Exception as e:
                raise ResourceCreationError(f"Unable to create new group {read_write.name}.\n{e}")
            if update_group:
                try:
                    if not dry_run:
                        ToolGlobals.client.iam.groups.delete(update_group)
                        print(f"  [bold green]OK[/] - Deleted old group {update_group}.")
                    else:
                        print(f"  [bold green]OK[/] - Would have deleted old group {update_group}.")
                except Exception as e:
                    raise ResourceDeleteError(f"Unable to delete old group {update_group}.\n{e}")

    def check_function_service_status(
        self, ToolGlobals: CDFToolConfig, token_inspection: TokenInspection, cdf_project: str, dry_run: bool
    ) -> None:
        print("Checking function service status...")
        has_function_read_access = not ToolGlobals.client.iam.compare_capabilities(
            token_inspection.capabilities,
            FunctionsAcl([FunctionsAcl.Action.Read], FunctionsAcl.Scope.All()),
            project=cdf_project,
        )
        if not has_function_read_access:
            self.warn(HighSeverityWarning("Cannot check function service status, missing function read access."))
            return None
        try:
            function_status = ToolGlobals.client.functions.status()
            if function_status.status != "activated":
                if function_status.status == "requested":
                    print(
                        "  [bold yellow]INFO:[/] Function service activation is in progress (may take up to 2 hours)..."
                    )
                else:
                    print(
                        "  [bold yellow]INFO:[/] Function service has not been activated, would have activated (will take up to 2 hours)..."
                    )
            else:
                print("  [bold green]OK[/] - Function service has been activated.")
        except CogniteAPIError as e:
            self.warn(HighSeverityWarning(f"Unable to check function service status.\n{e}"))

        return None
