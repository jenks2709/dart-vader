<<<<<<< HEAD
from models.member import Member
from repositories.member_repository import MemberRepository


class MemberAlreadyRegisteredError(Exception):
    pass


class MemberService:
    def __init__(self, repository: MemberRepository) -> None:
        self._repository = repository

    async def register_member(
        self,
        discord_user_id: int,
        guild_id: int,
        first_name: str,
        last_name: str,
        display_name: str,
    ) -> Member:
        existing_member = await self._repository.get_by_discord_id(
            discord_user_id,
            guild_id,
        )

        if existing_member is not None:
            raise MemberAlreadyRegisteredError()

        return await self._repository.create(
            discord_user_id=discord_user_id,
            guild_id=guild_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
        )
    async def list_members(
        self,
        *,
        guild_id: int,
    ) -> list[Member]:
=======
from models.member import Member
from repositories.member_repository import MemberRepository


class MemberAlreadyRegisteredError(Exception):
    pass


class MemberService:
    def __init__(self, repository: MemberRepository) -> None:
        self._repository = repository

    async def register_member(
        self,
        discord_user_id: int,
        guild_id: int,
        first_name: str,
        last_name: str,
        display_name: str,
    ) -> Member:
        existing_member = await self._repository.get_by_discord_id(
            discord_user_id,
            guild_id,
        )

        if existing_member is not None:
            raise MemberAlreadyRegisteredError()

        return await self._repository.create(
            discord_user_id=discord_user_id,
            guild_id=guild_id,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
        )
    async def list_members(
        self,
        *,
        guild_id: int,
    ) -> list[Member]:
>>>>>>> 70ee258 (Connecting traspberry pi and fix minor version compatability issues)
        return await self._repository.list_by_guild(guild_id=guild_id)