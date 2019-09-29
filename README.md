# Exercise 3

This assignment is due by 11:59PM ET 9/29.

# Submission Instructions

1. Fork this repository from the GitHub page.
2. Clone the repository to your computer using git so that you have your own copy to edit and submit.
1. Complete the assignment. Write your responses to the questions in this README.
5. Using git, commit your scripts, the output PDF and csv files, and your written answers.
6. Using git, push your code to your forked repository.
7. On GitHub, create a pull request to submit your work.


# Instructions

Each design will take some time to optimize. I recommend approaching the homework by

1. writing the scripts for each design, using a small number of cycles (`cycles=10`)
2. submit each of the scripts as jobs on the cluster to make sure everything works
3. Once everything runs for 10 cycles, increase cycles to 5000 and submit jobs for each part of the homework at once (but please answer the questions before looking at all the outputs). For 5000 cycles, 10 hours is probably a safe amount of time to request on the cluster.


This homework is computationally intensive, so it is important that you allow plenty of time to debug any problems in your scripts and leave time for the calculations to run. Unfortunately the computation time you need is completely unrelated to how much caffeine you can consume the night before the homework is due.


# Part 1

Generate a design with

- 5 minute length
- 2 equiprobable conditions
- The contrast of condition 1 minus condition 2
- order 1 counterbalancing
- optimized for detection efficiency only

The python script to do this is included as `optimize_part1.py`, but you will need to supply the sbatch script to run the code on the cluster (name this as `sbatch_part1.sh`) and increase the number of cycles to 5000 on line 17. 

## Output

- `part1_Xconv.pdf` shows the design matrix (after convolution with the HRF). Each column of the design (i.e. condition) is shown in a different color
- `part1_X.pdf` shows which condition is on over time (in TRs). $Y$ values of 1 indicate that the first condition is presented; 2 indicates the second condition, etc.
- `part1.csv` has the trial onset information, including an ITI column which gives the time interval to wait before showing the stimulus (the first value of 0 means the first stimulus should be presented immediately, since there is no previous onset)


## Question 1.1

In theory, you are optimizing a rapid event related design. Looking at the output, **what general type of design has the algorithm converged on?** In other words, does the general timing pattern remind you of something other than a rapid event related design?

Spoiler: your design could be broadly characterized as having the features of something other than a rapid event-related design, although the design may have not converged to the ideal form of this other type of design. 

The general type of design the algorithm converged on was the block type design. Even though the output is not completely a block design, there are chunks of stimulus 0 presentations and then chunks of stimulus 1 presentations. 


## Question 1.2

Speculate on why the optimal design you have obtained is in some respects uncharacteristic of a rapid event-related design. Specifically, consider

1. What effect is the lack of counterbalancing having here? What would you predict if equal weight were given to detection efficiency and 3rd order counterbalancing?
2. What effect does the number of conditions have here? What would you predict if there were 6 conditions?

You will investigate these questions in the next sections, but please answer these questions before looking at your results from part 2 & 3.

1. The lack of counterbalancing means that the algorithm won't worry about predictability of stimuli. This is why we get blocks of stimuli rather than alternating stimuli aperiodically. I would expect the stimuli to change more frequently than in this design if equal weight were given to detection efficiency and 3rd order counterbalancing.
2. Since there are only two conditions, a block design is efficient. If there were 6 conditions, I would expect a design more characteristic of a rapid event-related design because it would be hard to get the blocks of events we want to compare close to each other sequentially. 

# Part 2

Modify the design from Part 1 to

- use 3rd order counterbalancing (`confoundorder=3`)
- equally weight detection efficiency and counterbalancing (`weights=[0,.5,0,.5]`)

Also change `exercise = 'part2'` on line 20 of the script. Save the python script as `optimize_part2.py` and the sbatch script as `sbatch_part2.sh`

## Question 2.1

Compared to the result of Part 1, does this design qualitatively seems to be more of a rapid event-related design?

Yes, it appears so.

## Question 2.2

Are the differences between this design and Part 1 consistent with your earlier predictions?

Somewhat. There is less alternating than I expected towards the end (so it is still somewhat like a block design), but there is more interleaving of the stimuli towards the beginning of the design. 


# Part 3

Modify the design from Part 1 to

- have 6 equiprobable conditions
- contrast condition 1 vs 2 (note the contrast vector needs to have 6 elements, one per condition)


Also change `exercise = 'part3'` on line 20 of the script. Save the python script as `optimize_part3.py` and the sbatch script as `sbatch_part3.sh`


 
#Part 4

The previous designs were constructed to illustrate how design timing changes under different constraints and are unlikely to reflect practical design problems. Now we consider a moderately complex design that is realistic.

Modify Part 1 to optimize a design with:

- 5 conditions
- contrasts to compare conditions 1-2; 3-4; and (1+2)-(3+4). Remember that contrast vectors should sum to 0 when comparing different conditions.
- use exponential ITIs with min=1s, mean=2s, max=5s
- 3rd order counterbalancing
- equal weighting of design efficiency and counterbalancing (`weights=[0,.5,.5,0]`).


Also change `exercise = 'part4'` on line 20 of the script. Save the python script as `optimize_part4.py` and the sbatch script as `sbatch_part4.sh`


In part 3, you generated a design with 6 conditions, 4 of which were not included in any contrast, which is not very realistic—why would you include 4 extra (expensive) conditions of no interest in a real experiment? Here condition 5 is not included in any contrast, but this is reasonably plausible—these trials might be baseline periods in the design, filler trials, or response trials of no experimental interest. 

A real example of this type of design would be an audiovisual reading experiment with conditions:

1. auditory words
2. auditory nonwords
3. printed words
4. printed nonwords
5. 'catch' trials which require the participant to respond to a particular stimulus as an attention check, but are not of experimental interest

The contrasts give us:

- auditory words vs auditory nonwords (1-2)
- printed words vs printed nonwords (3-4)
- auditory vs visual (1+2)-(3+4)

allowing us to identify brain regions sensitive to lexicality effects within modalities and those sensitive to modality overall.

## Question 4.1

As we have discussed in class, it can be important to control for expectation in an experiment, which is accomplished through the `confoundorder` parameter and optimization weighting. One example of good counterbalancing comes from *m-sequences*, a special class of designs with high entropy and estimation efficiency. A true m-sequence is defined for $p$ conditions, where $p$ is prime, and generates a sequence of $p^k-1$ trials that are counterbalanced to the $k$th order. This means that for every window of $k$ trials, we will see all possible condition orders an equal number of times. For example if $k=5$ and we take a sliding window of 5 trials, we will see conditions orders of $1,1,1,1,1$; $1,1,1,1,2$; $1,1,1,1,2,3$, etc.

This is a very good thing statistically, but it may be undesirable psychologically (e.g. it might be very dull to see the same condition $k$ times in a row). This may also be problematic physiologically due to possible *adaptation* effects, in which repeated presentations of the same stimulus may suppress neural activity. 

**Q: Does the structure of this design seem desirable from both a psychological expectation and neural adaptation perspective? If not, is there a parameter in the [src.neurodesign.experiment class documentation](https://neurodesign.readthedocs.io/en/latest/genalg.html#neurodesign-design-optimisation) that might be useful to change?**

One parameter that limits the number of times a stimulus can be repeated is `maxrep`. The parameter is an integer (or `None`) indicating the maximum number of repetitions. However, for the most part, the structure of the design from Part 4 does not seem as if there is a stimuli that is presented too many times in a row. The most that I can tell is 4 times in a row. Every other "block" of conditions are only one or two presentations of the stimuli. 

