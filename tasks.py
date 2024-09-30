import os
from celery import Celery
from celery.utils.log import get_task_logger
from scripts import download_video, process_video, upload_to_supabase, update_supabase

app = Celery('tasks', broker=os.getenv("CELERY_BROKER_URL"))
logger = get_task_logger(__name__)


@app.task
async def process_video_job(url):
    video_path = ""
    clips = []

    try:
        video_path, video_id = await download_video(url)
        if video_path:
            clips = await process_video(video_path, video_id)

        upload_to_supabase(url, video_id, video_id, video_path, {}, clips)

        update_supabase(url, video_id, video_path, clips)
    finally:
        if video_path:
            os.remove(video_path)

        for clip in clips:
            os.remove(clip['path'])
    return {
        "url": url,
        "video_id": video_id,
        "video_path": video_path,
        "clips": clips
    }
