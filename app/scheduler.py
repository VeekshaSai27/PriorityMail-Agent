from apscheduler.schedulers.blocking import BlockingScheduler
from app.main import process_inbox
import os

scheduler = BlockingScheduler()

interval = int(os.getenv("SCHEDULE_MINUTES", "10"))
scheduler.add_job(process_inbox, "interval", minutes=interval)

if __name__ == "__main__":
    print(f"🔁 Running email agent every {interval} minutes...")
    scheduler.start()
