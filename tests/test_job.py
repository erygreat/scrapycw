from scrapycw.helpers.spider import JobHelper

def test_job_handler_close():
    job_helper = JobHelper("20210701_201135_zjomBasjPvjj")
    return job_helper.handler_when_close()