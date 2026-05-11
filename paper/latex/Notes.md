Notes:

I have a point I want to make but I don't know how best to change the paper to convey this. the point is that benchmark results change even when all parameters are unchanged due to the nature of LLMs. using greedy decoding (setting the temperature to zero) doesn't work, since (i) it doesn't guarantee determinism and most importantly (ii) several reasoning models fail when temperature = 0 (see https://arxiv.org/html/2512.12895v1). So the best practice, although expensive, is to run the same benchmark with the same configuration as many times as viable until a performance distribution can be obtained and thus a better understanding of the performance can be achieved (e.g., by checking the mean, median, and standard deviation). Maybe running it multiple times as described above is more of a side, practical recommendation than anything. But showing the problem is important. for instance, look at the figs/aider-polyglot-results.png (the results between the best and the worst runs can be pretty big, especially in this unfortunate but real era of "benchmaxing" where every decimal point counts). 

-----------

Leaderboards are broken by definition (by just showing numbers instead of distributions)
Check LeaderboardsOPS from Jimmy

Cannot force reproducible results with temp = 0 because
- it doesn't guarantee full reproducibility
- it hurts performance, since temp=0 is different than model's optimal setting 
- some reasoning models get locked in loops

We do need to have multiple runs and report them well
- show how many providers only report a number in HF

Check Anthropic bloom for a good example

---------

Add a top paper as reference and mention in Claude.md
Check MCP/plugin for citation (low priority)

--------

Many of these are well-known experimental and empirical software engineering principles that somehow are not being applied

----------------------------

DeepResearch is costly
There's a new paper/survey/thing everyday
Analysis must be systematic according to criteria that matters in practice

-------

Standardized timeout mechanisms

-------

For the benchmark selection paper -> start by showing how CLaude is actually far from being the best one in competition benchmarks (people believed that competition benchmarks was the way to go. except claude sucks on it yet it is cnosidered perhaps the best model for coding)