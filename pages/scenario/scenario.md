# Scenario Analysis{: .text-center .color-primary .mb-4}

<|navbar|>

<|card|

## Scenario Configuration{: .color-primary .mb-3}

<|layout|columns=3 1 1 1 1|gap=3|
<|{scenario}|scenario_selector|>

<|part|
**Prediction date**{: .color-primary} <br/>
<|{day}|date|active={scenario}|not with_time|>
|>

<|part|
**Max capacity**{: .color-primary} <br/>
<|{max_capacity}|number|active={scenario}|>
|>

<|part|
**Number of predictions**{: .color-primary} <br/>
<|{n_predictions}|number|active={scenario}|>
|>

<|part|
<br/>
<|Save|button|on_action=save|active={scenario}|>
|>
|>
|>

<|card|

## Scenario Details{: .color-primary .mb-3}

<|{scenario}|scenario|on_submission_change=submission_change|>
|>

<|card|

## Predictions Visualization{: .color-primary .mb-3}

<|{predictions_dataset}|chart|x=Date|y[1]=Historical values|type[1]=bar|y[2]=Predicted values ML|y[3]=Predicted values Baseline|height=400px|width=100%|>
|>
