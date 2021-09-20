from flask import Flask, render_template, request  
import pickle
import numpy as np
# from flask_ngrok import run_with_ngrok

app = Flask(__name__)
# run_with_ngrok(app)

# Load the TF-IDF vocabulary specific to the category
with open(r"toxic_vect.pkl", "rb") as f:
    tox = pickle.load(f)

with open(r"severe_toxic_vect.pkl", "rb") as f:
    sev = pickle.load(f)

with open(r"obscene_vect.pkl", "rb") as f:
    obs = pickle.load(f)

with open(r"insult_vect.pkl", "rb") as f:
    ins = pickle.load(f)

with open(r"threat_vect.pkl", "rb") as f:
    thr = pickle.load(f)

with open(r"identity_hate_vect.pkl", "rb") as f:
    ide = pickle.load(f)

# Load the pickled RDF models
with open(r"toxic_model.pkl", "rb") as f:
    tox_model = pickle.load(f)

with open(r"severe_toxic_model.pkl", "rb") as f:
    sev_model = pickle.load(f)

with open(r"obscene_model.pkl", "rb") as f:
    obs_model  = pickle.load(f)

with open(r"insult_model.pkl", "rb") as f:
    ins_model  = pickle.load(f)

with open(r"threat_model.pkl", "rb") as f:
    thr_model  = pickle.load(f)

with open(r"identity_hate_model.pkl", "rb") as f:
    ide_model  = pickle.load(f)

# Render the HTML file for the home page
@app.route("/",methods=['GET','POST'])
def home():
    result = {}
    if request.method == 'POST':
        message = request.form['message']
        result = predict(message)
        return render_template('index.html', result=result)
    return render_template('index.html', result=result)

def predict(message):
    
    # Take a string input from user
    user_input = message
    data = [user_input]

    vect = tox.transform(data)
    pred_tox = tox_model.predict_proba(vect)[:,1]

    vect = sev.transform(data)
    pred_sev = sev_model.predict_proba(vect)[:,1]

    vect = obs.transform(data)
    pred_obs = obs_model.predict_proba(vect)[:,1]

    vect = thr.transform(data)
    pred_thr = thr_model.predict_proba(vect)[:,1]

    vect = ins.transform(data)
    pred_ins = ins_model.predict_proba(vect)[:,1]

    vect = ide.transform(data)
    pred_ide = ide_model.predict_proba(vect)[:,1]

    out_tox = round(pred_tox[0], 2)
    out_sev = round(pred_sev[0], 2)
    out_obs = round(pred_obs[0], 2)
    out_ins = round(pred_ins[0], 2)
    out_thr = round(pred_thr[0], 2)
    out_ide = round(pred_ide[0], 2)

    print(out_tox)

    result ={}

    result['Probability of being a Toxic comment: '] = out_tox,
    result['Probability of being a Severely toxic comment: '] = out_sev, 
    result['Probability of being an Obscene comment: '] = out_obs,
    result['Probability of being an Insult: '] =  out_ins,
    result['Probability of being a Threat: '] = out_thr,
    result['Probability of being an Identity Hate comment: '] = out_ide                        
    
    return result
     
# Server reloads itself if code changes so no need to keep restarting:
if __name__ == "__main__":
    app.run()
