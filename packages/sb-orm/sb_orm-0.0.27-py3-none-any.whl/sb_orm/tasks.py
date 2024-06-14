import aiohttp
import asyncio
from datetime import datetime
from .Db import DatabaseSession
from .models import Task, TaskStatus
from .config import env
import json


db_session = DatabaseSession()
db_prefix = env("DB_PREFIX")
task_table = f"{db_prefix}{env('TASKS_TABLE', 'tasks')}"


async def perform_task(task_id: int):
    async with db_session.get_session() as session:
        task_query = db_session.db(task_table).where({'id': task_id})
        task = await task_query.find()
        if not task:
            return

        async with aiohttp.ClientSession() as client_session:
            for _ in range(task['times']):
                try:
                    result = await fetch_url(client_session, task)
                    await save_result_and_notify(task, result)
                except Exception as e:
                    await handle_task_failure(task, e)
                await asyncio.sleep(task['frequency'])

        await finalize_task_completion(task)


async def fetch_url(session, task):
    if task['method'].upper() == "GET":
        async with session.get(task['target_url'], headers=task.get('header')) as response:
            return await response.text()
    elif task['method'].upper() == "POST":
        async with session.post(task['target_url'], json=task.get('post_body'), headers=task.get('header')) as response:
            return await response.text()
    else:
        raise ValueError("Unsupported HTTP method")


async def save_result_and_notify(task, result):
    async with db_session.get_session() as session:
        task['last_result'] = result
        task['times_completed'] += 1
        await session.commit()

    async with aiohttp.ClientSession() as client_session:
        async with client_session.post(task['callback_url'], json={"result": result}) as callback_response:
            await callback_response.text()


async def handle_task_failure(task, error):
    async with db_session.get_session() as session:
        task['status'] = TaskStatus.FAILED
        task['error_message'] = str(error)
        await session.commit()


async def finalize_task_completion(task):
    async with db_session.get_session() as session:
        task['status'] = TaskStatus.COMPLETED
        task['completed_at'] = datetime.utcnow()
        await session.commit()


async def create_task(task_data):
    async with db_session.get_session() as async_session:
        session = async_session.session  # 获取内部的 Session 对象
        post_body = json.dumps(task_data['post_body'])
        header = json.dumps(task_data['header'])
        task = Task(
            target_url=task_data['target_url'],
            method=task_data['method'],
            post_body=post_body,
            header=header,
            frequency=task_data['frequency'],
            times=task_data['times'],
            callback_url=task_data['callback_url']
        )
        session.add(task)  # 在 Session 对象上调用 add 方法
        await session.commit()
        await session.refresh(task)
        return task


async def get_task_status(task_id):
    async with db_session.get_session() as session:
        task_query = db_session.db(task_table).where({'id': task_id})
        task = await task_query.find()
        return task if task else None
