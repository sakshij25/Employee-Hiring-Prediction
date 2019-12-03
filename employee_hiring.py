
from flask import Flask, render_template, request
from sklearn.externals import joblib
import numpy as np

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('index.html')

def ls_prediction(salaryhike,env_satisfaction,worklife,years):
    model = joblib.load("EMP_PERFORMANCE_RATING.sav")
    prediction = model.predict([[salaryhike,env_satisfaction,worklife,years]])
    return prediction

def ls_prediction1(overtime,age,joblevel):
    model = joblib.load("EMP_ATTRITION.sav")
    prediction = model.predict([[overtime,age,joblevel]])
    return prediction

@app.route("/rating", methods=['POST', 'GET'])
def rating():
    if (request.method == 'POST'):
        values = request.form
        print(values)
        emp_id = int(values['EmployeeID'])
        salaryhike = values['EmpLastSalaryHikePercent']
        env_satisfaction = values['EmpEnvironmentSatisfaction']
        worklife = values['EmpWorkLifeBalance']
        years = values['YearsSinceLastPromotion']
        salaryhike = np.int64(int(salaryhike))
        env_satisfaction = np.int64(int(env_satisfaction))
        worklife = np.int64(int(worklife))
        years = np.int64(int(years))
        perf_ratings = ls_prediction(salaryhike,env_satisfaction,worklife,years)
        message ="Employee ID: " + str(emp_id) + "\tPerformance Rating: " +str(perf_ratings)
        return message
    else:
        return render_template('index1.html')

@app.route("/attrition", methods=['GET', 'POST'])
def attrition():
    if (request.method == 'POST'):
        values = request.form
        print(values)
        emp_id = int(values['EmployeeID'])
        overtime = values['OverTime']
        age = values['Age']
        joblevel = values['EmpJobLevel']
        overtime = np.int64(int(overtime))
        age = np.int64(int(age))
        joblevel = np.int64(int(joblevel))
        attri = ls_prediction1(overtime,age,joblevel)
        message ="Employee ID: " + str(emp_id) + "\tAttrition: " +str(attri)
        return message
    else:
        return render_template('index2.html')

if __name__ == '__main__':
    app.run()