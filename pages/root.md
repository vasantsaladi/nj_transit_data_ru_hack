<|navbar|>

# Welcome to NJ Transit Data Analysis

This is the home page of our application.

<|layout|columns=1 1 1|gap=2rem|
<|card|

### Daily Ridership

<|metric|value=total_ridership|format=,.0f|>
|>

<|card|

### On-Time Performance

<|metric|value=on_time_percentage|format=.1f%|>
|>

<|card|

### Active Routes

<|metric|value=active_routes|format=,.0f|>
|>
|>

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

.selector {
    border: 1px solid #1B2C5B;
    border-radius: 4px;
    padding: 0.5rem;
}

.button {
    background-color: #1B2C5B;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.5rem 1rem;
    cursor: pointer;
}

.button:hover {
    background-color: #2d4580;
}

.table thead th {
    background-color: #1B2C5B;
    color: white;
}

.table tbody td {
    border-bottom: 1px solid #1B2C5B20;
}
</style>
