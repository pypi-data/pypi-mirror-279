import asyncio


def sync_run(fn):
    """
    Run an async func in sync func
    """

    loop = asyncio.get_event_loop()
    if loop.is_running():
        return loop.run_until_complete(fn)
    else:
        return asyncio.run(fn)
