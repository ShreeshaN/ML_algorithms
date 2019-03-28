# Description
Information Value Analysis is a Data Exploration technique that helps determine which data columns in a dataset have predictive power or influence on the value of a specified Dependent Variable. It has been a popular method for alerting banks, for example, of determining a set of variables best at capturing which credit card customers are most likely to default.


#### Information Value (IV)
A numerical value which quantifies the predictive power of an independent continuous variable x in capturing the binary dependent variable y. IV is helpful for reducing the number of variables as an initial step in preparing for Logistic Regression, especially when there are a large amount of potential variables. 

IV is based on an analysis of each individual independent variable in turn without considering other predictor variables.

#### Weight of Evidence (WOE)
Closely related to the IV value, WOE measures the strength of each grouped attribute in predicting the desired value of the Dependent Variable

 

#### Algorithm
Formulae for calculating Information Value (IV) and Weight of Evidence (WOE): 

___Weight of Evidence = Ln(Distribution Good/Distribution Bad)*100___ 

___Information Value = sum((Distribution Good - Distribution Bad)*Ln(Distribution Good/Distribution Bad)___

where Distribute Good refers to percentage of values, for each given independent variable grouping, that results in the desired "Value to Predict" for the dependent variable and Distribution Bad is the percentage of values within each grouping that is not the "Value to Predict"

__Standards for using the Information Value to understand the predictive power of each Variable.__ 

| Information Value |  Predictive Capability |
| ----------------- | ----------------------- |
| Above 0.5 | Suspiciously good; too good to be true |
| 0.3 - 0.5 | Strong predictive capability |
| 0.1 - 0.3 | Medium predictive capability |
| 0.02 - 0.1 |	Weak predictive capability |
| Below 0.02 | Useless |

References:
1. https://www.youtube.com/watch?v=XVjq45YSjsY
2. https://alpine.atlassian.net/wiki/spaces/V6/pages/107544700/Information+Value
3. https://github.com/kingspp/algo-stats
