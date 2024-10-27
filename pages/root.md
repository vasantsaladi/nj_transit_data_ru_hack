<|navbar|>

<|part|class_name=text-center mb-4|
![NJ Transit Logo](assets/NJ_Transit_Logo.png){: width=300px}
|>

# Welcome to NJ Transit Data Analysis{: .text-center .color-primary .mb-4}

<|layout|columns=1 1 1|gap=2rem|
<|card|

### Daily Ridership{: .color-primary}

<|metric|value=total_ridership|format=,.0f|>
|>

<|card|

### On-Time Performance{: .color-primary}

<|metric|value=on_time_percentage|format=.1f%|>
|>

<|card|

### Active Routes{: .color-primary}

<|metric|value=active_routes|format=,.0f|>
|>
|>

<|card|

## Quick Navigation{: .color-primary .mb-3}

<|layout|columns=1 1 1|gap=4|
<|Navigate to Data Visualization|button|link=/data_viz|>
<|Create New Scenario|button|link=/scenario|>
<|View Performance Analysis|button|link=/performance|>
|>
|>
</code_block_to_apply_changes_from>

<style>
.card {
    background-color: #FFFFFF;
    border: 1px solid #1B2C5B;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

h3 {
    color: #1B2C5B;
    margin-bottom: 0.5rem;
}

.metric {
    font-size: 24px;
    font-weight: bold;
    color: #1B2C5B;
}

.button {
    background-color: #1B2C5B;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    width: 100%;
}

.button:hover {
    background-color: #2d4580;
}

.mb-4 {
    margin-bottom: 1.5rem;
}

.mt-4 {
    margin-top: 1.5rem;
}

.text-center {
    text-align: center;
}

.color-primary {
    color: #1B2C5B;
}
</style>
