from covid import Covid
from datetime import datetime

cov = Covid()
country_list = [i['name']
                for i in sorted(cov.list_countries(), key=lambda x:x['name'])]
