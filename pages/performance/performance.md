<|navbar|>

# Performance Analysis{: .text-center .color-primary .mb-4}

<|part|render={len(comparison_scenario)>0}|
<|card|

## Scenario Comparison{: .color-primary .mb-3}

<|Table|expanded=False|expandable|
<|{comparison_scenario}|table|>
|>
|>

<|card|

## Metric Selection{: .color-primary .mb-3}

<|{selected_metric}|selector|lov={metric_selector}|dropdown|>

<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=RMSE baseline|y[2]=RMSE ML|render={selected_metric=="RMSE"}|height=400px|width=100%|>

<|{comparison_scenario}|chart|type=bar|x=Scenario Name|y[1]=MAE baseline|y[2]=MAE ML|render={selected_metric=="MAE"}|height=400px|width=100%|>
|>
|>

<|card|
<|Compare Scenarios|button|on_action=compare|>
{: .text-center}
|>
