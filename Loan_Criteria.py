from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime

app = Flask(__name__)

def evaluate_loan_application(savings_account_balance, applicant_credit_score, 
                            existing_monthly_debt, yearly_gross_income, requested_loan_duration):
    """
    Evaluates a loan application based on multiple financial factors
    Returns a comprehensive risk assessment score and personalized feedback
    """

    total_risk_assessment_points = 0 #points assigned based on many criteria 
    MAX_POSSIBLE_POINTS = 1000 #upper limit of points
    
    EXCELLENT_CREDIT_THRESHOLD = 750
    GOOD_CREDIT_THRESHOLD = 650
    FAIR_CREDIT_THRESHOLD = 550
    
    if applicant_credit_score >= EXCELLENT_CREDIT_THRESHOLD:
        total_risk_assessment_points += 300
    elif applicant_credit_score >= GOOD_CREDIT_THRESHOLD:
        total_risk_assessment_points += 200
    elif applicant_credit_score >= FAIR_CREDIT_THRESHOLD:
        total_risk_assessment_points += 100
        
    monthly_income = yearly_gross_income / 12
    monthly_debt_ratio = (existing_monthly_debt / monthly_income) * 100 #ratio of debt to income
    
    CONSERVATIVE_DEBT_RATIO = 20
    MODERATE_DEBT_RATIO = 35
    RISKY_DEBT_RATIO = 45
    
    if monthly_debt_ratio <= CONSERVATIVE_DEBT_RATIO:
        total_risk_assessment_points += 250
    elif monthly_debt_ratio <= MODERATE_DEBT_RATIO:
        total_risk_assessment_points += 150
    elif monthly_debt_ratio <= RISKY_DEBT_RATIO:
        total_risk_assessment_points += 50
        
    financial_safety_ratio = (savings_account_balance / yearly_gross_income) * 100 #ratio of savings to income
    
    EXCELLENT_SAVINGS_RATIO = 50
    GOOD_SAVINGS_RATIO = 25
    MINIMUM_SAVINGS_RATIO = 10
    
    if financial_safety_ratio >= EXCELLENT_SAVINGS_RATIO:
        total_risk_assessment_points += 250
    elif financial_safety_ratio >= GOOD_SAVINGS_RATIO:
        total_risk_assessment_points += 150
    elif financial_safety_ratio >= MINIMUM_SAVINGS_RATIO:
        total_risk_assessment_points += 50
        
    HIGH_INCOME_THRESHOLD = 75000 #income threshold for high income
    MEDIUM_INCOME_THRESHOLD = 45000 #income threshold for medium income
    LOW_INCOME_THRESHOLD = 25000 #income threshold for low income
    
    if yearly_gross_income > HIGH_INCOME_THRESHOLD:
        total_risk_assessment_points += 200
    elif yearly_gross_income > MEDIUM_INCOME_THRESHOLD:
        total_risk_assessment_points += 150
    elif yearly_gross_income > LOW_INCOME_THRESHOLD:
        total_risk_assessment_points += 100
        
    final_risk_score = (total_risk_assessment_points / MAX_POSSIBLE_POINTS) * 100 #final score
    
    #Generate detailed recommendation
    if final_risk_score >= 80:
        detailed_feedback = "Strong application! Your financial profile indicates excellent creditworthiness and stable income. High likelihood of approval with competitive rates."
    elif final_risk_score >= 60:
        detailed_feedback = "Positive application overall. Your financial metrics are generally good, though some aspects might benefit from improvement. Moderate to good approval chances."
    elif final_risk_score >= 40:
        detailed_feedback = "Mixed application results. While some aspects of your profile are strong, others raise some concerns. Additional documentation or collateral may be required."
    else:
        detailed_feedback = "Challenging application status. Several key metrics fall below our standard thresholds. Consider improving your credit score or reducing existing debt before applying."
    
    return {
        "application_score": round(final_risk_score, 2),
        "detailed_feedback": detailed_feedback,
        "evaluation_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/check_eligibility', methods=['POST'])
def process_loan_application():
    application_data = request.json
    
    evaluation_result = evaluate_loan_application(
        float(application_data['current_balance']),
        float(application_data['credit_score']),
        float(application_data['current_loans']),
        float(application_data['income']),
        float(application_data['loan_term'])
    )
    return jsonify(evaluation_result)

if __name__ == '__main__':
    app.run(debug=True) 