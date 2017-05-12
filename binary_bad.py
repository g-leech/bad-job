badJobCycle =	0.5		# 6 months average tenure of a bad job  
goodJobCycle =	4 		# 4 years average tenure of a good job  

badCandidateCycle =	0.2	
goodCandidateCycle = goodJobCycle 

badJobRate = 0.6		# % of jobs that are bad
badCandidRate = 0.6		# % of candidates that are bad

hiringAccuracy = 0.5
jobSearchAccuracy = 0.5

searchTime = 0.4		# Time between advert and first day

candPool = 100000
jobPool = 10000


from rand import rand 


class LabourUnit( object ):
	def __init__( self, isGood ):
		self.isGood = isGood

    def get_good():
    	return self.isGood


class Job( LabourUnit ):
	def __init__( self, candidate, isGood ):
		LabourUnit.__init__(isGood)
		self.hire = candidate	

	def get_hire():
		return self.hire

	def set_hire(hire):
		self.hire = hire

	def fire():
		self.get_hire().set_job() = None
		self.set_hire( None )


class Candidate( LabourUnit ):
	def __init__( self, job, isGood ) :
		LabourUnit.__init__(isGood)
		self.job = job	

	def get_job() :
		return self.job

	def set_job(job) :
		self.job = job

	def quit() :
		self.get_job().set_hire( None )
		self.set_job( None )


def gen_job( jobs ):
	isGood = False if ( rand() <= badJobRate ) else True
	jobs.append(Job(True, isGood))


def gen_candidate( cands ):
	isGood = False if ( rand() <= badCandidRate ) else True
	cands.append(Candidate(False, isGood))


#
def hiring( jobs, candidates ):
	openJobs = [ job for job in jobs if job.get_hire() is None ]

	for job in openJobs:
		


# Good hires shed bad jobs
def career_progression( jobs ):
	badJobs = [ job for job in jobs if not job.get_good() ]

	for job in badJobs:
		hire = job.get_hire()
		if hire.get_good():
			hire.quit()


# Good jobs shed mishires (as do half of bad jobs)
def downsize( jobs ):
	goodJobs = [ job for job in jobs if job.get_good() ]

	for job in goodJobs:
		if not job.get_hire().get_good():
			job.fire()

	badJobs = [ job for job in jobs if not job.get_good() ]

	for job in badJobs:
		spottedByHr = rand() < hiringAccuracy
		if not job.get_hire().get_good() and spottedByHr:
			job.fire()				



# generate jobs
jobs = []
jobs = [ gen_job(jobs) for i in range(jobPool) ] 

# generate candidates
candidates = []
candidates = [ gen_candidate(candidates) for i in range(candPool) ]


for tick in range(100):
	career_progression()
	downsize()
	hiring()

	openJobs = [ job for job in jobs if job.get_hire() is None ]
	badOpenJobs = [ job for job in openJobs if not job.get_good() ]
	print(str(len(badOpenJobs)/jobPool) + "\% of open jobs are bad")


print("For a market where bad jobs turn over every " + str(badJobCycle*12) +" months and ")
print("good jobs turn over every " + str(goodJobCycle*12) +" months, the steady-state percentage ")
print("of all available jobs that are bad is " + str(badOpenJobCount/jobPool) )


# This behaviour is stable over a wide range of values
for i in range(10):
	badCandidRate = i/10
	# Run all



# Average quality of applicants:
# Average quality of jobs:


# Obvious extensions: 
# * grades of quality; 
# * isomorphic job/candidate fit (Head of Customer Service is a bad job for me, while data scientist is a terrible job for you);
# * skills scarcity / glut
# * accuracy of vetting process