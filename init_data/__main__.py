import asyncio
from aiohttp import ClientSession
import aiofiles
from aiocsv import AsyncReader
import time


async def create_document_request(
        text: str, rubrics: list, created_date: str, session: ClientSession
) -> None:
    url = "http://127.0.0.1:8000/v1/documents"
    body = {
        'rubrics': rubrics,
        'text': text,
        'created_date': created_date
    }

    async with session.post(url, json=body) as resp:
        print(resp.status)


def str_to_rubric_list(string: str) -> list[str]:
    return [
        string.strip("'")
        for string in string.lstrip('[').rstrip(']').split(', ')
    ]


async def load_csv_and_request() -> None:
    tasks = []

    async with ClientSession() as session:
        async with aiofiles.open('posts.csv', 'r') as f:
            reader = AsyncReader(f)
            await anext(reader)

            async for line in reader:
                tasks.append(
                    asyncio.create_task(
                        create_document_request(
                            text=line[0],
                            created_date=line[1],
                            rubrics=str_to_rubric_list(line[2]),
                            session=session
                        )
                    )
                )

            for task in tasks:
                await task


if __name__ == '__main__':
    prev_time = time.time()

    asyncio.run(load_csv_and_request())

    cur_time = time.time()
    print(cur_time - prev_time)
