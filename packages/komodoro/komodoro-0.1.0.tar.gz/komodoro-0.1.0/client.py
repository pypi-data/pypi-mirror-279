from httpx import AsyncClient


async def main():
    async with AsyncClient() as client:
        response = await client.get("http://localhost:8000/")
        response.raise_for_status()

        response = await client.get("http://localhost:8000/2")
        response.raise_for_status()

        response = await client.get("http://localhost:8000/3")
        response.raise_for_status()

        response = await client.get("http://localhost:8000/path/John")
        response.raise_for_status()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
