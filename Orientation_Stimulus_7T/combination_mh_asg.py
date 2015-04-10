import random
import copy
import itertools
import numpy as np

def combination_for_run(n_null=10, n_cond=4, n_observations=5):
	# number of NULL events	
	# number of conditions	
	# number of observations per condition


	# make sequence template
	seq = list(itertools.chain(*[[i] * n_observations  for i in range(1, n_cond + 1)]))

	# dummy to speed things up
	for_sampling = range(len(seq))

	cur_seqs = [copy.copy(seq) for h in ('lh', 'rh')]
	random.shuffle(cur_seqs[0])
	random.shuffle(cur_seqs[1])


	while True:
		sample_space=random.sample(for_sampling, n_null)
		sample_space.sort()
		if 1 not in [x - sample_space[i - 1] for i, x in enumerate(sample_space)][1:]:
			break
	#print sample_space
	sample_space=[i+x for i, x in enumerate(sample_space)]
	for idx in sample_space:
		hemisphere=random.randint(0,1)
		cur_seqs[hemisphere].insert(idx, cur_seqs[hemisphere][idx])
		cur_seqs[hemisphere^1].insert(idx + 1, 0)
		
	lh=cur_seqs[0]
	rh=cur_seqs[1]
	
	'''
	print 'LH:', seq[0]
	print 'RH:', seq[1]

	for seq, d in ((lh, 'lh'), (rh, 'rh')):
		for i, s in enumerate(seq):
			fh = open('%s_%i.log' % (d, s), 'a')
			fh.write('%f 3.0 1\n' % (16 * i + 0))
			#onset_time.append(trial_length * i + jitter[i])
			fh.close()
	'''
	combined_seqs=zip(cur_seqs[0],cur_seqs[1])
	return combined_seqs
	
if __name__ == '__main__':
	combination_for_run()