"""Admin state for user management."""

from __future__ import annotations

from AMM_web.graphql import gql
from AMM_web.models.user import UserSummary
from AMM_web.state.base_state import BaseState


class AdminUsersState(BaseState):
    users: list[UserSummary] = []
    total_users: int = 0
    auth_error: str | None = None
    success_message: str | None = None

    new_username: str = ""
    new_email: str = ""
    new_password_hash: str = ""
    new_role: str = "USER"
    new_is_active: bool = True

    def _reset_messages(self) -> None:
        self.set_error(None)
        self.auth_error = None
        self.success_message = None

    @staticmethod
    def _error_message(data: dict, fallback: str) -> str:
        errors = data.get("errors") or []
        if errors:
            return errors[0].get("message", fallback)
        return fallback

    async def load_users(self, access_token: str = "", is_admin: bool = False) -> None:
        self.set_loading(True)
        self._reset_messages()
        if not is_admin:
            self.auth_error = "Admin access required."
            self.users = []
            self.total_users = 0
            self.set_loading(False)
            return
        if not access_token:
            self.auth_error = "Authentication required."
            self.users = []
            self.total_users = 0
            self.set_loading(False)
            return

        query = """
        query Users($limit: Int!, $offset: Int!) {
          users(limit: $limit, offset: $offset) {
            total
            items { id username email role isActive firstName lastName }
          }
        }
        """
        try:
            data = await gql(
                query,
                variables={"limit": 200, "offset": 0},
                access_token=access_token,
            )
        except Exception as exc:
            self.set_error(str(exc))
            self.set_loading(False)
            return

        if "errors" in data:
            self.set_error(self._error_message(data, "Failed to load users"))
            self.users = []
            self.total_users = 0
            self.set_loading(False)
            return

        payload = ((data.get("data") or {}).get("users") or {})
        self.total_users = int(payload.get("total", 0))
        self.users = [UserSummary(**item) for item in payload.get("items", [])]
        self.set_loading(False)

    async def create_user(self, access_token: str = "", is_admin: bool = False) -> None:
        self._reset_messages()
        if not is_admin:
            self.auth_error = "Admin access required."
            return
        if not access_token:
            self.auth_error = "Authentication required."
            return
        if not self.new_username.strip() or not self.new_email.strip() or not self.new_password_hash.strip():
            self.set_error("Username, email, and password hash are required.")
            return

        mutation = """
        mutation CreateUser($data: UserCreateInput!) {
          createUser(data: $data) { id }
        }
        """
        variables = {
            "data": {
                "username": self.new_username.strip(),
                "email": self.new_email.strip(),
                "passwordHash": self.new_password_hash.strip(),
                "role": self.new_role,
                "isActive": self.new_is_active,
            }
        }
        try:
            data = await gql(mutation, variables=variables, access_token=access_token)
        except Exception as exc:
            self.set_error(str(exc))
            return

        if "errors" in data:
            self.set_error(self._error_message(data, "Failed to create user"))
            return

        self.success_message = "User created."
        self.new_username = ""
        self.new_email = ""
        self.new_password_hash = ""
        self.new_role = "USER"
        self.new_is_active = True
        await self.load_users(access_token, is_admin)

    async def set_user_role(
        self,
        user_id: int,
        role: str,
        access_token: str = "",
        is_admin: bool = False,
    ) -> None:
        self._reset_messages()
        if not is_admin:
            self.auth_error = "Admin access required."
            return
        if not access_token:
            self.auth_error = "Authentication required."
            return

        mutation = """
        mutation UpdateUserRole($userId: Int!, $data: UserUpdateInput!) {
          updateUser(userId: $userId, data: $data) { id role }
        }
        """
        variables = {"userId": user_id, "data": {"role": role}}
        try:
            data = await gql(mutation, variables=variables, access_token=access_token)
        except Exception as exc:
            self.set_error(str(exc))
            return

        if "errors" in data:
            self.set_error(self._error_message(data, "Failed to update user role"))
            return

        self.success_message = "User role updated."
        await self.load_users(access_token, is_admin)

    async def set_user_active(
        self,
        user_id: int,
        is_active: bool,
        access_token: str = "",
        is_admin: bool = False,
    ) -> None:
        self._reset_messages()
        if not is_admin:
            self.auth_error = "Admin access required."
            return
        if not access_token:
            self.auth_error = "Authentication required."
            return

        mutation = """
        mutation UpdateUserActive($userId: Int!, $data: UserUpdateInput!) {
          updateUser(userId: $userId, data: $data) { id isActive }
        }
        """
        variables = {"userId": user_id, "data": {"isActive": is_active}}
        try:
            data = await gql(mutation, variables=variables, access_token=access_token)
        except Exception as exc:
            self.set_error(str(exc))
            return

        if "errors" in data:
            self.set_error(self._error_message(data, "Failed to update user status"))
            return

        self.success_message = "User status updated."
        await self.load_users(access_token, is_admin)

    async def delete_user(self, user_id: int, access_token: str = "", is_admin: bool = False) -> None:
        self._reset_messages()
        if not is_admin:
            self.auth_error = "Admin access required."
            return
        if not access_token:
            self.auth_error = "Authentication required."
            return

        mutation = """
        mutation DeleteUser($userId: Int!) {
          deleteUser(userId: $userId) { id }
        }
        """
        try:
            data = await gql(mutation, variables={"userId": user_id}, access_token=access_token)
        except Exception as exc:
            self.set_error(str(exc))
            return

        if "errors" in data:
            self.set_error(self._error_message(data, "Failed to delete user"))
            return

        self.success_message = "User deleted."
        await self.load_users(access_token, is_admin)
