def print_viewed_jobs(fromUser  = 'Default', jobs = []):
    with open('jobs_viewed.txt', 'a') as file:
        for job in jobs:
            file.write(job['jobkey'])
    print 'The number of jobs is %i' % in_state
    result = [job['jobkey'] for job in jobs]
    if fromUser != 'Default':
        return result
    else:
        return 'check your input'


def compute_cosine_similarity(jobkey):
    return 


def return_two_nearest_results(fromUser  = 'Default', jobs = []):
    return