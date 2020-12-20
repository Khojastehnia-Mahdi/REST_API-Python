# Mahdi Khojastehnia - Dec 19, 2020 
# khojastehnia.m@gmail.com - mkhoj015@uottawa.ca


# --------------------------------------------------------------------
# REST API: Its inputs are the age, weight, and height of a person. 
# Then it returns two outputs:
# 1- It shows whether the risk for severe disease from COVID-19 is 
# high ( age > 65 or BMI > 30) or  there is not enough information
# in order to determine it.
# 2- The body mass index (BMI) categories: 
# Underweight - Normal weight - Overweight - Obesity


# ---------------------------------------------------------------------
import time
import numpy as np
from flask import Flask, jsonify, request


# Creating a class to represent the data of a person.
class personData:
    
    def __init__(self, age, weight, height):
        self.age = age
        self.weight = weight
        self.height = height

    # This is the private method that returns the value of BMI.
    def __getBMI(self):
        return self.weight / (self.height**2)
    
    # This is the method that returns the BMI Category.
    def getBMI_Cat(self):
        if self.__getBMI() < 18.5 :
            return 'Underweight'
        elif 18.5 <= self.__getBMI() < 25 :
            return 'Normal weight'
        elif 25 <= self.__getBMI() < 30 :
            return 'Overweight'
        elif 30 <= self.__getBMI() :
            return 'Obesity'

    # This is the method that returns the risk for severe 
    # disease from COVID-19.
    def riskCovid19(self):
        if (self.age >= 65 or self.__getBMI() >= 30) :
            return True
        else:
            return False



# REST API
app = Flask(__name__)


# The route of the api
@app.route('/BMI_Covid19', methods=['POST'])
def determine():
        # json fields
        if request.is_json:
            age_val = request.json['age']
            weight_val = request.json['weight']
            height_val = request.json['height']

        # form fields    
        else:
            age_val = request.form['age']
            weight_val = request.form['weight']
            height_val = request.form['height']
            
        # Converting strings to floats for two cases:
        # 1- request.json: when values are strings (not floats); 
        # 2- request.form 
        try:
            age_float = float(age_val)
            weight_float = float(weight_val)
            height_float = float(height_val)

            # Raising an error if one of the values are negative.
            if (age_float > 0 and weight_float > 0 and height_float > 0):
                
                # risk for disease for the associated person?
                pData = personData(age = age_float , 
                        weight = weight_float, height = height_float)
                if pData.riskCovid19():
                    return jsonify(high_Vulnerability_COVID19 = "True",
                                   BMI_Category = pData.getBMI_Cat()), 200
                else:
                    return jsonify(
                    high_Vulnerability_COVID19 = "Not enough information",
                                  BMI_Category = pData.getBMI_Cat()), 200
            else:
                return jsonify(message = 
                "Values of age, weight and height must be positive."), 406
        except:
            return jsonify(message = 
            "The data must include numbers, not supporting letters or symbols."), 406


# debug
if __name__ =="__main__":  
    app.run(debug = True) 

        



