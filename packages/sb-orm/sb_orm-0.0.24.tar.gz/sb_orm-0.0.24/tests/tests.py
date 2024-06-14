import asyncio
import pytest
from sb_orm import tasks


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_create_task():
    # 构造任务数据
    task_data = {
        'target_url': 'https://apphwhq.longhuvip.com/w1/api/index.php',
        'method': 'POST',
        'post_body': {
            'a': 'GetStockPanKou_Narrow',
            'c': 'StockL2Data',
            'StockID': '600435',
            'State': '1'
        },
        'header': None,
        'frequency': 1,  # 每次请求之间的间隔秒数
        'times': 3,  # 总请求次数
        'callback_url': ''
    }
    # 调用创建任务函数
    task = await tasks.create_task(task_data)
    # 验证任务是否成功创建
    assert "id" in task
    assert "status" in task


@pytest.mark.asyncio
async def test_get_task_status():
    # 假设这里有一个有效的任务 ID
    task_id = 1
    # 调用获取任务状态函数
    task = await tasks.get_task_status(task_id)
    # 验证获取任务状态是否成功
    assert task is not None
    assert "id" in task
    assert "status" in task

# 添加更多测试用例来覆盖其他函数和边缘情况
