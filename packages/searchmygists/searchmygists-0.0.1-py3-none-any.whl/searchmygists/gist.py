import msgspec
import httpx
from functools import cached_property


class Gist(msgspec.Struct):
    id: int
    gh_id: str
    name: str
    description: str
    owner: str
    public: bool
    starred: bool
    content: str
    tags_str: str
    extensions_str: str
    filenames_str: str
    # created_at: date
    # updated_at: date

    @cached_property
    def tags(self) -> list[str]:
        return self.tags_str.split(",")

    @cached_property
    def extensions(self) -> list[str]:
        return self.extensions_str.split(",")

    @cached_property
    def filenames(self) -> list[str]:
        return self.filenames_str.split(",")


async def get_user_gists(gh_token: str) -> list[Gist]:
    gists = []
    async with httpx.AsyncClient(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {gh_token}",
                "X-GitHub-Api-Version": "2022-11-28",
                "Accept": "application/vnd.github+json"
            },
    ) as client:
        raw_gists = client.get("/gists")

    return gists
