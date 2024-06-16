from cwstorm.examples.lib import nodes


def get_job():
    job = nodes.make_job_node()
    
    # create an upload scene task
    upload_scene = nodes.make_upload_scene_node()

    # Create frames and ass export for 5 chunks of 4 frames.
    # Each ass export writes 4 frames, since it's pretty fast
    chunks = 10
    chunk_size = 2
    frame = 0
    frame_tasks = []
    for i in range(chunks):
        start_frame = i * chunk_size
        end_frame = i * chunk_size + chunk_size - 1

        ass = nodes.make_ass_node(start_frame, end_frame)
        ass.add(upload_scene)

        for j in range(chunk_size):
            frame_task =nodes.make_frame_node(frame)
            job.add(frame_task)
            upload_tex = nodes.make_upload_tex_node(frame)
            frame_task.add(ass)
            ass.add(upload_tex)

            frame_tasks.append(frame_task)
            frame += 1

    return job
