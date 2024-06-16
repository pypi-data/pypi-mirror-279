
from cwstorm.examples.lib import nodes


def get_job():
    
    job = nodes.make_job_node()
    quicktime = nodes.make_quicktime_node()
    job.add(quicktime)
    return job
