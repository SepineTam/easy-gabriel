# Easy-GABRIEL
An easier way for social science researchers to use OpenAI-GABRIEL. 

## Why Built it?
OpenAI-GABRIEL is cool, but it is a little difficult for researchers who are not familiar with Python, especially when using Non-OpenAI models.
Also, as of now, the official project only has a README and a Jupyter file to demonstrate how to use it, lacking a proper documentation.
Therefore, I aim to provide a simpler way to use it from the third-part model providers like DeepSeek and so on.

## How to Use?
### Install
You can use uv or pip install this project: 
```bash
uv add easy-gabriel
# or, if you do not prefer uv, using pip
pip install easy-gabriel
```

### Use in Python
In order to minimize migration cost, you could refer the following code:  
```python
import os

import pandas as pd
from easy_gabriel import EasyGABRIEL, init_gabriel, run_gabriel


gabriel: EasyGABRIEL = init_gabriel(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    model="deepseek-chat",
    response="openai",  # it is means the model is adapted to OpenAI API format. 
)

# Then, all the action is same as the official package. 
# For example, if we want to use gabriel.rate

df: pd.DataFrame  # your dataset
attributes: dict[str, str]  # your attributes config

gabriel_func = gabriel.rate(
    df, 
    column_name="your_col_name",
    attributes=attributes,
    save_dir="./output",
    model="deepseek-chat",  # if you are not set model, it would be used by previous setting in init_gabriel()
)

result: pd.DataFrame = run_gabriel(gabriel_func)

```


