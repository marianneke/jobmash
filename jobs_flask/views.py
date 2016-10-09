from flask import render_template, request
from jobs_flask import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import random
import re
import ast
import pandas as pd
import psycopg2

from utilities import remember_viewed_jobs

user = 'marianne'             
host = 'localhost'
dbname = 'indeed_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user)
jobs_seen = []
jobkeys_picked = []

@app.route('/')

@app.route('/employers')
def find_candidate_type():
  #pull 'job title' from input field and store it
  job_description = request.args.get('description')
  # PREDICT JOBTITLE FOR THIS TEXT
  return render_template("employers.html", job_description = job_description)

@app.route('/input')
def jobsearch_input():
    #jobs_seen = []
    return render_template("input.html")#, jobs_seen=jobs_seen)

@app.route('/output', methods=['POST', 'GET'])
def jobsearch_output():
  if request.method == 'GET':
    # empty list of jobs seen and jobs picked
    jobs_seen = []
    jobkeys_picked = []
    #pull 'job title' from input field and store it
    search_jobtitle = request.args.get('jobtitle')
    #pull 'state' from input field and store it
    search_loc = request.args.get('state')
    #print search_loc
    #just select the jobs from the indeed database for the state and jobtitle that the user inputs
    query = "SELECT jobkey, jobtitle, url, company, description FROM indeed_jobs_top50 WHERE LOWER(jobtitle) LIKE lower('%s') AND LOWER(state) LIKE lower('%s')  ORDER BY RANDOM() LIMIT 2" % (search_jobtitle, search_loc)
  if request.method == 'POST':
    # pull 'jobs_seen' from button and store it
    jobs_seen = request.form['jobs_seen']
    jobs_seen = ast.literal_eval(jobs_seen)
    #pull 'jobkey_choice' from button and store it
    jobkey_choice = request.form['jobkey_choice']
    try:
      jobkeys_picked.append(jobkey_choice)
    except:
      jobkeys_picked = [jobkey_choice]
    print jobkey_choice
    #get text for jobkey_choice
    try:
      query_choice = "SELECT tf_lsi15_top50 FROM indeed_jobs_top50 WHERE jobkey = '%s'" % jobkey_choice
      query_result = pd.read_sql_query(query_choice,con)
      print "Got top-50 for selected job"
      top_50_similar = re.findall("\(\'([a-zA-Z0-9]+)\'\,", query_result.iloc[0]['tf_lsi15_top50'] )#.replace("{", "").replace("}","")
      print "top 5:", top_50_similar[:5]
      #print "Jobs seen:", len(jobs_seen)
      try:
        top_50_unseen = [job for job in top_50_similar if job not in jobs_seen]
      except:
        top_50_unseen = top_50_similar
      print "Length", len(top_50_unseen)
      print "Removed jobs in history from top 50"
      #then pick the 2 most similar that are not in jobs_seen
      jobkeys_similar = random.sample(top_50_unseen, 2)
      print "Similar jobkeys to pick:", jobkeys_similar[0], jobkeys_similar[1]
      #select these two jobs from the database
      query = "SELECT jobkey, jobtitle, url, company, description FROM indeed_jobs_top50 WHERE jobkey = '%s' OR jobkey = '%s' LIMIT 2" % (jobkeys_similar[0], jobkeys_similar[1])
    except:
      print "One of the queries didn't work"
      return render_template("input.html") #, jobs_seen = jobs_seen)
  try:
    #print query
    query_results=pd.read_sql_query(query,con)
    print "Query successful"
    jobs = []
    for i in range(0,2): #query_results.shape[0]):
      try:
        jobs_seen.append({'jobkey': query_results.iloc[i]['jobkey'], 'url': query_results.iloc[i]['url'], 'jobtitle': query_results.iloc[i]['jobtitle'], 'company': query_results.iloc[i]['company']})
      except:
        print "Error with appending jobs seen"
        # jobs_seen = [{'jobkey': query_results.iloc[i]['jobkey'], 'url': query_results.iloc[i]['url'], 'jobtitle': query_results.iloc[i]['jobtitle'], 'company': query_results.iloc[i]['company']}]
      print "Appended jobs seen", len(jobs_seen)
      jobs.append(dict(jobkey=query_results.iloc[i]['jobkey'], jobtitle=query_results.iloc[i]['jobtitle'], url=query_results.iloc[i]['url'], company=query_results.iloc[i]['company'], description=query_results.iloc[i]['description']))
    # Remove duplicates from jobs_seen list
    #jobs_seen = list(set(jobs_seen))
    print "jobs seen:", jobs_seen
    jobs_seen_str = str(jobs_seen).replace(" ", "")
    return render_template("output.html", jobs = jobs, jobs_seen = jobs_seen, jobs_seen_str = jobs_seen_str)
  except:
    print "Query unsuccesful"
    return render_template("input.html")