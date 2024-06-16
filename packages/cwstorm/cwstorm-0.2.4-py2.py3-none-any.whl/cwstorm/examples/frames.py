from cwstorm.examples.lib import nodes



def get_job():
    job = nodes.make_job_node()

    # create an upload scene task
    upload_scene = nodes.make_upload_scene_node()

    # Create frames and ass export for 5 chunks of 4 frames.
    # Each ass export writes 4 frames, since it's pretty fast
    chunks = 10
    chunk_size = 5
    frame = 0
    for i in range(chunks):
        start_frame = i * chunk_size
        end_frame = i * chunk_size + chunk_size - 1

        frame_task = nodes.make_frame_range_node(start_frame, end_frame)
        upload_tex = nodes.make_upload_tex_range_node(start_frame, end_frame)
        frame_task.add(upload_tex)
        frame_task.add(upload_scene)
        job.add(frame_task)
        frame += chunk_size

    return job
