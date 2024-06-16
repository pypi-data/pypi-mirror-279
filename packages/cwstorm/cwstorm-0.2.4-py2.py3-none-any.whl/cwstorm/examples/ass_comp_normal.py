
from cwstorm.examples.lib import job_types


def get_job():
    """Make a job."""
    return job_types.get_ass_to_comp_job(chunks=4, chunk_size=5)
