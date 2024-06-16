from cwstorm.examples.lib import job_types

def get_job():
    return job_types.get_sim_render_qt_job(10)
