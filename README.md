# corona-model

[Wiki  ](https://github.com/corona-python/corona-model/wiki)
[Download  ](https://github.com/corona-python/corona-model/releases)
[Presentation  ](https://github.com/corona-python/corona-model/blob/master/corona.pdf)

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
 
 ### _Which model has the least severe economic impact?_
