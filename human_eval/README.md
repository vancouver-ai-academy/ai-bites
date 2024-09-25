## Overview

This is a human evaluation platform called JudgeOsiris, named after the "judge of the dead" of ancient Egypt.

## Quick Start

### 1. Run Web App

```
python app.py -m1 <path to model 1 predictions> 
              -m2 <path to model 2 predictions> 
              -o <folder where results are saved>
```

**Caveat:** `m1` and `m2` are paths that should be under "static"


### 2. Click on generated url to get an image like the one below

Choose which output you prefer from the models




### 3. To customize the app for your human eval task, you need to change two things

Change this file to include the things you want to add
`human_eval/templates/fragments/model_result.html`

Change 

Change 