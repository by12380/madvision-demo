import os
from flask import Flask, flash, render_template, redirect, request
from tasks import process_video_job
from scripts import ensure_test_urls_in_supabase

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', "super-secret")


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/batch-process', methods=['POST'])
def batch_process():
    urls = request.form['urls'].split('\r\n')
    ensure_test_urls_in_supabase(urls)

    task_ids = []

    for url in urls:
        response = process_video_job.delay(url)
        task_ids.append(response.id)

    task_ids_joined = "\n".join(task_ids)
    flash(f"Your addition job has been submitted.\n{task_ids_joined}")

    return redirect('/')
