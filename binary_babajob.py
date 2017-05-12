
timeToSplit = 0.2		# the fundamental frequency of the market. 10 weeks here.

badJobCycle =	0.5		# 6 months average tenure of a bad job  
goodJobCycle =	3 		# 3 years average tenure of a good job  

badCandidateCycle =	timeToSplit
goodCandidateCycle = goodJobCycle 

badJobRate = 0.6		# % of jobs that are bad
badCandidRate = 0.6		# % of candidates that are bad

hiringAccuracy = 0.5
jobSearchAccuracy = 0.5

searchTime = 0.4		# Time between advert and first day

candPool = 100000
jobPool = 10000


# p(hired | bad) = p(bad | hired) * p(hired) / p(bad)


from random import random


class LabourUnit( object ):
	def __init__( self, isGood ) :
		self.isGood = isGood

	def get_good(self) :
		return self.isGood


class Job( LabourUnit ):
	def __init__( self, candidate, isGood ):
		LabourUnit.__init__(self, isGood)
		self.hire = candidate	

	def get_hire(self):
		return self.hire

	def set_hire(self, hire):
		self.hire = hire
		if hire :
			self.hire.set_job( self )

	def fire(self):
		self.hire.quit()


class Worker( LabourUnit ):
	def __init__( self, job, isGood ) :
		LabourUnit.__init__(self, isGood)
		self.job = job	
		self.tenure = 0

	def get_job(self) :
		return self.job

	def set_job(self, job) :
		self.job = job

	def quit(self) :
		self.job.set_hire( None )
		self.set_job( None )
		self.tenure = 0


def gen_job():
	isGood = False if ( random() <= badJobRate ) else True
	return Job(None, isGood)


def gen_worker():
	isGood = False if ( random() <= badCandidRate ) else True
	return Worker(None, isGood)


def filter_good_jobs(jobs):
	return [ job for job in jobs if job.get_good() ]


def filter_bad_jobs(jobs):
	return [ job for job in jobs if not job.get_good() ]

#
def hiring( jobs, candidates ):
	openJobs = [ job for job in jobs if job.get_hire() is None ]
	openCandidates = [ cand for cand in candidates if cand.get_job() is None ]

	for job in openJobs:
		for candidate in openCandidates:
			hrGuessRight = random() < hiringAccuracy
			if hrGuessRight:
				if candidate.get_good() :
					job.set_hire(candidate)
					break
			else :
				if not candidate.get_good() :
					job.set_hire(candidate)
					break


# Good hires shed bad jobs
def ditch_bad_jobs( jobs ):
	for job in filter_bad_jobs(jobs) :
		hire = job.get_hire()
		if hire and hire.get_good() :
			hire.quit()


def leave_good_jobs( jobs ):
	for job in jobs:
		hire = job.get_hire()
		if hire and hire.tenure > goodJobCycle:
			hire.quit()


# Good jobs shed mishires (as do half of bad jobs)
def prune_bad_hires( jobs ):
	goodJobs = [ job for job in jobs if job.get_good() ]

	for job in filter_good_jobs(jobs):
		hire = job.get_hire()

		if hire and not hire.get_good():
			job.fire()


	for job in filter_bad_jobs(jobs):
		spottedByHr = random() < hiringAccuracy
		hire = job.get_hire()
		if hire and not hire.get_good() and spottedByHr:
			job.fire()				


def labour_occurs( candidates, tick ):
	employees = [cand for cand in candidates if cand.get_job() is not None]

	for emp in employees:
		emp.tenure += tick


def update_market(jobs, candidates):
	ditch_bad_jobs( jobs )
	leave_good_jobs( jobs )
	prune_bad_hires( jobs )
	hiring( jobs, candidates )
	labour_occurs( candidates, timeToSplit )


# generate jobs
jobs = []
jobs = [ gen_job() for i in range(jobPool) ] 

# generate candidates
candidates = []
candidates = [ gen_worker() for i in range(candPool) ]



for tick in range(100):
	update_market(jobs, candidates)

	openJobs = [ job for job in jobs if job.get_hire() is None ]
	badOpenJobs = [ job for job in openJobs if not job.get_good() ]
	print(str(len(badOpenJobs)/jobPool) + "\% of open jobs are bad")


print("For a market where bad jobs turn over every " + str(badJobCycle*12) +" months and ")
print("good jobs turn over every " + str(goodJobCycle*12) +" months, the steady-state percentage ")
print("of all available jobs that are bad is " + str(badOpenJobCount/jobPool) )


# Average quality of all jobs:
# Average quality of all workers:
# Average quality of applicants:
# Average quality of open jobs:



# This behaviour is stable over a wide range of values
for i in range(10):
	badCandidRate = i/10
	# Run all




# Obvious extensions: 
# * grades of quality; 
# * isomorphic job/candidate fit (Head of Customer Service is a bad job for me, while data scientist is a terrible job for you);
# * skills scarcity / glut
# * accuracy of vetting process