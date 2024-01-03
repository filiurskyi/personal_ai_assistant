from celery import shared_task
from bot.bot import main
import asyncio

@shared_task
def run_framework(var):
    print("====================================== running")
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

@shared_task
def restart_framework(var):
    print("====================================== restart framework")

@shared_task
def stop_framework(var):
    print("====================================== stop framework")

@shared_task
def terminate_framework(var):
    print("====================================== terminate framework")
