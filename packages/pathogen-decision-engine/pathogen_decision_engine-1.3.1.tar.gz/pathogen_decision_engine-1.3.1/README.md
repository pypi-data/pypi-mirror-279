# Pathogen Decision Engine Package

The Decision Engine Package is a Python package for building and using decision engines based on rule sets defined in CSV files.
Its main purpose is to implement the decision mechanism described in the SOVAD [^1] paper to classify the pathogenicity of a mutation given a well-known set of predictors.

Twin project using GoRules' zen-engine : [sovad-gorules](https://github.com/bergo-bioinfo/sovad_gorules)


## Installation

You can install the package via pip:

    pip install pathogen-decision-engine

or building the module locally

    pip install -e .

## Usage

### Command-Line Interface (CLI)

The package provides a command-line interface (CLI) for performing inference using the decision engine. 

To use the CLI, you can provide either the path of a rule table path made as a CSV file. The engine expect a rule table file made of a table of shape N x M+1 where N is the number of rules, M is the number of predictors and +1 is referring to the classification label for each rule. 
Each cell can be empty or filled with a symbol (>, >=, ==, <, <=) and a value, indicating a numeric constraint for a certain predictor regarding a certain rule.
Example:

    decision_engine_cli --rule_table_path data/sovad_rules_table.csv --input_sample '{"PA":1, "PVS":0, "PS":1, "PM":2, "PP":1, "BA":1, "BS":0, "BP":0}'

You can pass a rule table in the form of dict expressed as a string
Example:

    decision_engine_cli --rule_table_dict "{'PA':{'0':1,'1':0},'PVS':{'0':0,'1':1},'PS':{'0':0,'1':'>=1'},'PM':{'0':0,'1':0},'PP':{'0':0,'1':0},'BA':{'0':0,'1':0},'BS':{'0':0,'1':0},'BP':{'0':0,'1':0},'Output':{'0':'Pathogenic','1':'Pathogenic','2':'Pathogenic'}}" --input_dict '{"PA":1, "PVS":0, "PS":1, "PM":2, "PP":1, "BA":1, "BS":0, "BP":0}'


### Python API

You can also use the package programmatically in your Python code. Here's an example of how to use the DecisionEngine class:

```python
from pathogen_decision_engine import PathogenDecisionEngine

df = None ### ... create a df dataframe as you wish

# Create a DecisionEngine object
decision_engine = PathogenDecisionEngine(df)

# Define input dictionary
input_sample = {"PA":1, "PVS":0, "PS":1, "PM":2, "PP":1, "BA":1, "BS":0, "BP":0}
# Or you can define your input as list of sovad predictors, then the engine will take care of the counting:
input_sample = ["PA2", "PS1", "PP4", "PM3" ] # in this case you can omit the predictors with 0 count

# Perform inference
result = decision_engine.infer(input_sample)
print(result)
```


## References
[^1] [Koeppel, Florence et al.] “[Standardisation of pathogenicity classification for somatic alterations in solid tumours and haematologic malignancies.](doi:10.1016/j.ejca.2021.08.047)” [European journal of cancer (Oxford, England : 1990) vol. 159 (2021): 1-15]. 
