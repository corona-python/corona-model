# corona-model

Downloads:
[Source and Windows Exe, ](https://github.com/corona-python/corona-model/releases)
[Presentation](https://github.com/corona-python/corona-model/blob/master/corona.pdf)

# What if you could change the world?

## Options
![Options](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/options.PNG)

This program is intended to explore the political choices available to confront a pandemic.
Each choice involves a policy decision that has life or death consequences. 
- Do we spend tax money on testing or do we give tax breaks to the rich in an election year?
- Do we focus on early containment/mitigation or gamble with the hope that it will just go away?
- How many deaths will occur as a result of our decision?

_Hover over menu items to see a brief description of parameters_

Influential Parameters:
- Percent sick traced outside lockdown
- Days of denial
- Early end of lockdown
- How quickly we react to lockdown changes (attack/decay)
- Days before test results
- Lessons learned
- Health care quality (percent sick who die)

Number of infections is estimated as 2X number of govt. reported cases.
This is due to large number of asymptomatic cases and inconsistent reporting.
Lockdown attack/decay is implemented as simple first order recursive section.
Test tracing is weighted inversely by days to results.

This code may be modified and distributed freely as long as this header is included at the top
of this code and any derived code

## USA Current Trend
![USA Current](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/usa.png)

## Taiwan Current Trend
### 43 Million People, Few Deaths, What Did They Do Differently?
![USA Current](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/taiwan.png)
 
 ### _Which response has the least severe economic impact?_
 
 ## What if it takes 5 days for test results?
![USA Five Days](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/usa_5_no_random.png)

 ## Or 1 Day?
![USA One Day](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/usa_1_no_random.png)

 ## Then, what if we add just 0.1% random testing of the population?
 ### With better testing after lockdown ends, we'd save 80,000 lives.
![USA One Day](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/usa_1_random.png)

 ## What if we responded more aggresively, 30 days earlier?
 ### We could have flattened the curve.
 ![Faster Response](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/fast.png)


## My USA model may be optimistic, we are not flattening the curve as of May 3
At least, at this point, thanks to lockdown, case growth appears more linear than exponential. When lockdown is lifted, without deployment of lessons learned (testing, etc), we will go back to exponential.

[Image: Johns Hopkins Coronavirus Resource Center](https://coronavirus.jhu.edu/data/cumulative-cases)
![countries](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/countries_may3.png)

## Limitations
#### Simulation Time Delta
I've used a very simple infection model, R infections per day per person. Once R infections have spread by a single source, 
the source no longer infects. This is reasonable in the average of 330 Million people. An interesting experiment is to 
randomize the R value and you will find that chance can have a dramatic impact, however the trends for testing, 
lockdown, tracing, etc remain consistent.

#### True Number of Cases
Things get interesting here. While the replication factor changes as mitigation and containment measure are introduced, 
I could never correlate the conventional estimate for R0 (2.2 to 2.6) with any reasonable model based on puublished number of cases. 
In my opionion, the number of actual cases is a minimum of 2X and more likely 4X what is being reported by CDC. I may re-calibrate the model based on 4X reported cases instead of 2X as shown here.

#### Attack/Decay
How quickly the transistions to and from lockdown occur can have a major impact on the number of infections. The model uses
a simple filter to emulate a 



