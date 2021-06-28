# How to submit jobs on htcondor

	1. You'll need a current python version. Unfortunately, the version on the server is not regularly updated, so I would recommend to go with `miniconda`.
	2. To run your experiment, run `. 1_setup.sh` (and make sure you have conda activated). This will create a workspace with all the htcondor files.
	3. Go into every `batch_x` folder and run `condor_submit submitfile.sub` to submit the jobs of that batch.
	4. Check with `condor_q` that all your jobs were submitted successfully

Good luck with your experiments! :)
~ Rafael
