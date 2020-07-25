from flask import Flask,render_template,redirect, url_for,request,session,flash
from covid import Covid
cov = Covid()
from datetime import datetime
first = Flask(__name__,static_url_path="/static")
first.secret_key = "asfjbdsh"

country_list = [i['name'] for i in sorted(cov.list_countries(),key=lambda x:x['name'])]
id_list = [i['id'] for i in sorted(cov.list_countries(),key=lambda x:x['name'])]
unsorted_country_list = [i['name'] for i in cov.list_countries()]
 

@first.route("/",methods = ['POST','GET'])
def index():
    if request.method == "POST":
        name = request.form['name']
        if name in id_list:
            return redirect(url_for("country",ctry=name))
        else:
            flash("Seems like this is not a Country")
            return render_template("index.html",false_val = True,clist = cov.list_countries())

    else:
        return render_template("index.html",false_val=False,
                clist=sorted(cov.list_countries(),key=lambda x:x['name']))

@first.route("/<ctry>")
def country(ctry):
    stat = cov.get_status_by_country_id(str(ctry))
    total_conf = stat['confirmed']
    total_deaths = stat['deaths']
    ctry = stat['country']
    recs = stat['recovered']
    active = stat['active']
    perc = recs*100/(total_deaths+recs)
    time = datetime.fromtimestamp(stat['last_update']/1000)
    return render_template('covid_detail.html',country=ctry,total_conf=total_conf,
                        total_deaths=total_deaths,recs=recs,active=active,
                        time = time, perc=round(perc,2),rank = unsorted_country_list.index(ctry)+1)

if __name__ == '__main__':
    first.run(debug=True)
