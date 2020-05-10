# corona-model

[Download Latest Version](https://github.com/corona-python/corona-model/releases)

[Presentation](https://github.com/corona-python/corona-model/blob/master/corona.pdf)

[GitHub](https://github.com/corona-python/corona-model)

# How Would You Manage COVID-19?
Note: this model is being updated frequently as policies change, features are added and bugs are discovered. 
Check back often for latest updates.
## Options
![Options](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/options.PNG)

This program is intended to explore the political choices available to confront a pandemic.
Each choice involves a policy decision that has life or death consequences. 
- Do we spend tax money on testing or do we give tax breaks to the rich in an election year?
- Do we focus on early containment/mitigation or gamble with the hope that it will just go away?
- How many deaths will occur as a result of our decision?

Influential Parameters:
- How quickly we react to the crisis
- Percent sick traced outside lockdown
- Days of denial
- Early end of lockdown
- Days before test results
- Lessons learned
- Health care quality

Number of infections is estimated as 3X number of govt. reported cases. This is due to large number of undetected asymptomatic infections and inconsistent local, state and federal reporting.

## USA Current Trend
### This Assumes We Start Disciplined Testing and Isolation
![USA Current](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/usa.png)

### What If We Eliminated Testing?
![USA No Testing](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/no_testing.png)

### What If We Started Testing Earlier?
#### With better testing at start of lockdown, we'd save over 100,000 lives.
![USA No Testing](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/test_early.png)

## Early Test Results and Isolation Could Eliminate Need for General Lockdown
![Test GIF](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/output_7y4R8d.gif)

## Taiwan Current Trend
### 43 Million People, Few Deaths, What Did They Do Differently?
![USA Current](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/taiwan_flat.png)
 
## We Are Not Significantly Flattening the Curve
At least, at this point, thanks to lockdown, case growth appears more linear than exponential. When lockdown is lifted, without deployment of lessons learned (testing, etc), we will go back to exponential.

[May 9: Johns Hopkins Coronavirus Resource Center](https://coronavirus.jhu.edu/data/cumulative-cases)
![countries](https://raw.githubusercontent.com/wiki/corona-python/corona-model/images/countries_may9.png)

## [How Aggressive Do We Need to Be?](https://www.businessinsider.com/seoul-bars-and-clubs-closed-after-covid-19-cases-linked-2020-5)
``` The city of Seoul, South Korea, on Saturday ordered all bars and nightclubs in the city shut down indefinitely just three days after people in the city were told to begin "a new daily life with Covid-19."

According to a report from The New York Times, the closure comes after a 29-year-old man tested positive for COVID-19 on Wednesday after he visited three nightclubs in the Itaewon area in the city last weekend. As of Saturday, officials said they were tracking down more than 7,000 people who had visited five nightclubs in the region, according to the report.

"Just because of a few people's carelessness, all our efforts so far can go to waste," Seoul Mayor Park Won Soon said at a press conference Saturday.

According to The Times, the mayor said at least 40 infections had been linked to nightclubs, though Kwon Jun Wok, a senior disease-control official, said Saturday that just 27 reported cases had been linked to the venues.

Park said 40 cases included the 27 in Seoul, 12 in Gyeonggi Province and Incheon, and one in Busan, according to The Korea Herald.

South Korea has so far achieved a great deal of success in mitigating the virus without completely shutting down its economy, due in part to its rigorous testing and contact tracing strategies. But as The Times noted Saturday, the question now is whether South Korea can make a further shift toward normalcy without negating its success in flattening the curve. ```

## Discussion/Limitations
#### Simulation Time Delta
I've used a very simple infection model, R infections per day per person. Once R infections have spread by a single source, 
the source no longer infects. This is reasonable in the average of 330 Million people. An interesting experiment is to 
randomize the R value and you will find that chance can have a dramatic impact, however the trends for testing, 
lockdown, tracing, etc remain consistent.

#### True Number of Cases
Things get interesting here. While the replication factor changes as mitigation and containment measure are introduced, 
I could never correlate the conventional estimate for R0 (2.2 to 2.6) with any reasonable model based on published number of cases. 
In my opinion, the number of actual cases is a minimum of 2X and more likely 4X what is being reported by CDC. In the latest model, I have re-calibrated  to approximately 3X instead of 2X as shown earlier. As of May 4, news outlets are reporting that the true number could be as much as 10X government figures. This uncertainty is due to the lack of testing in USA. Without routine testing, we can only make our best guess as to the true numbers, however, this is primarily a problem with the absolute numbers being reported. Differential trends as a reaction to policy implementations (testing, lockdown, etc) will be largely unaffected. Confused and frustrated by the lack of a comprehensive federal plan for testing? Me too.

#### How Do We Model Transitions?
How quickly the transitions to and from lockdown occur can have a major impact on the number of infections. The model uses simple recursive sections to emulate transition times ( lockdown, testing, etc).

#### Days to Test Result
The percentage of people isolated after coming in contact with an infected person is attenuated by a "forgetting factor" determined by 1/N where N = number of days waiting for test results. 



