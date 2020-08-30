# Overview
This script helps analyze data exported from LinkedIn using the member data export capability. It's inspired by [this article](https://towardsdatascience.com/mining-data-on-linkedin-9b70681b1467).

It reads connections and surface random people distributed across companies and positions to help us stay in touch with people.

To export LinkedIn data, visit [this link](https://www.linkedin.com/psettings/member-data).

#### Usage
```
mkdir linkedin-analysis
<download and unzip the member data in this directory>
mv <LINKED_IN_DATA_DIR> exported
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
python linkedin_analysis.py --help
```
