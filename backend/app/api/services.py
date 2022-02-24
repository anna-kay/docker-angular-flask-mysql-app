from flask import Blueprint, Response, request, json, jsonify
import configparser
import os
from ..utils.questionnairesProcessor import QuestionnairesProcessor
from ..utils.recommendationsGenerator import RecommendationsGenerator
from ..database.dbManager import DBManager
from ..database.authManager import AuthManager

config = configparser.ConfigParser()
config.read('config.ini')

securityguideAPI = Blueprint('securityguideAPI', __name__)
endpoint = "/api"

app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

questionnaires_processor = QuestionnairesProcessor()
recommendations_generator = RecommendationsGenerator()
db_manager = DBManager()
auth_manager = AuthManager()

"""------------------------ RISK QUESTIONNAIRE -----------------------------"""
@securityguideAPI.route(endpoint + "/risk_questionnaire", methods=['GET'])
def risk_questionnaire():
    file_path = (os.path.join(app_path, "risk" ))    
    function = request.args.get('function')
    layer = request.args.get('layer')
    risk_questionnaire = file_path + '//risk_questionnaire.json'
    response = questionnaires_processor.get_risk_questions\
        (function, layer, risk_questionnaire)
    return jsonify(response)


@securityguideAPI.route(endpoint + "/risk_answers/email/<string:email>", methods=['POST', 'GET'])
def risk_questionnaire_answers(email):    
    if request.method == 'POST':
        req = request.get_json()
        db_manager.insert_risk_answers(email, req)
        return jsonify("Risk questionnaire answers were submitted")
    else:
        risk_answers = {}
        try:
            user = auth_manager.retrieve_user_by_email(email)
            risk_answers_tmp = db_manager.get_risk_answers(user['email'])  
            tmp = risk_answers_tmp[0][0]                  
            tmp = tmp.replace("\'", "\"")    
            risk_answers = json.loads(tmp)                
            risk_answers_2 = risk_answers['results']  
            response = Response(json.dumps(risk_answers_2), \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response


@securityguideAPI.route(endpoint + "/risk_results/email/<string:email>", methods=['GET'])
def get_risk_radarchart_scores(email):
    try:        
        user = auth_manager.retrieve_user_by_email(email)
        risk_answers = db_manager.get_risk_answers(user['email']) 
        tmp = risk_answers[0][0]                  
        tmp = tmp.replace("\'", "\"")              
        risk_answers = json.loads(tmp)              
        risk_answers_2 = risk_answers['results']        
        radarchart_scores = \
            questionnaires_processor.compute_radarchart_scores(risk_answers_2)                       
        response = Response(json.dumps(radarchart_scores), mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response


@securityguideAPI.route(endpoint + "/risk_targets/email/<string:email>", methods=['POST', 'GET'])
def risk_targets(email):
    if request.method == 'POST':
        req = request.get_json()
        results_dicts_list = req["results"]
        db_manager.insert_risk_targets(email, results_dicts_list)
        return jsonify("Risk target levels were submitted")
    else:
        risk_targets = []
        try:
            user = auth_manager.retrieve_user_by_email(email)
            risk_targets_tmp = db_manager.get_risk_targets(user['email'])
            tmp = risk_targets_tmp[0][0]
            tmp = tmp.replace("\'", "\"") 
            risk_targets = json.loads(tmp)
            processed_risk_targets = questionnaires_processor.process_risk_targets(risk_targets)
            risk_targets = json.dumps(processed_risk_targets)
            response = Response(risk_targets, \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response


"""----------------------- MATURITY QUESTIONNAIRE --------------------------"""
@securityguideAPI.route(endpoint + "/maturity_questionnaire", methods=['GET'])
def maturity_questionnaire():    
    file_path = (os.path.join(app_path, "maturity" ))
    # Load the questions in a dictionary
    with open(file_path + '//maturity_questionnaire.json', 'r') as f:
        quest_dictionary = json.load(f)
    return jsonify(quest_dictionary)


@securityguideAPI.route(endpoint + "/maturity_answers/email/<string:email>", methods=['POST', 'GET'])
def maturity_questionnaire_answers(email):   
    if request.method == 'POST':
        try:        
            req = request.get_json()         
            db_manager.insert_maturity_answers(email, req)
            response = jsonify("Maturity questionnaire answers were submitted")
        except Exception as e:
            response = handleException(e)
        finally:
            return response
    else:
        maturity_answers = {}
        try:
            user = auth_manager.retrieve_user_by_email(email)
            maturity_answers_tmp = db_manager.get_maturity_answers(user['email'])   
            tmp = maturity_answers_tmp[0][0]                    
            tmp = tmp.replace("\'", "\"")                 
            maturity_answers = json.loads(tmp)            
            response = Response(json.dumps(maturity_answers), \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response
    
    
@securityguideAPI.route(endpoint + "/maturity_results/email/<string:email>", methods=['GET'])
def get_maturity_results(email):
    maturity_results = []
    try:
        user = auth_manager.retrieve_user_by_email(email)
        maturity_answers_tmp = db_manager.get_maturity_answers(user['email'])       
        tmp = maturity_answers_tmp[0][0]
        tmp = tmp.replace("\'", "\"")
        maturity_answers = json.loads(tmp)        
        maturity_levels = questionnaires_processor.get_current_maturity_levels(maturity_answers, email)
        maturity_scores = questionnaires_processor.get_maturity_scores(maturity_answers)
        maturity_results.append(maturity_levels)
        maturity_results.append(maturity_scores)
        response = Response(json.dumps(maturity_results), mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response
    

@securityguideAPI.route(endpoint + "/maturity_targets/email/<string:email>", methods=['POST', 'GET'])
def get_maturity_targets(email):
    if request.method == 'POST':
        req = request.get_json()
        results_dicts_list = req["results"]
        db_manager.insert_maturity_targets(email, results_dicts_list)
        return jsonify("Maturity target levels were submitted")
    else:
        maturity_targets = {}
        try:
            user = auth_manager.retrieve_user_by_email(email)
            maturity_targets_tmp = db_manager.get_maturity_targets(user['email'])
            tmp = maturity_targets_tmp[0][0]
            tmp = tmp.replace("\'", "\"")
            maturity_targets = json.loads(tmp)
            response = Response(json.dumps(maturity_targets), \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response


"""----------------------- PRIORITY QUESTIONNAIRE --------------------------"""

@securityguideAPI.route(endpoint + "/priority_questionnaire", methods=['GET'])
def priority_questionnaire():  
    file_path = (os.path.join(app_path, "priority"))  
    #Load the questions in a dictionary
    with open(file_path + '//priority_questionnaire.json', 'r') as f:
        quest_dictionary = json.load(f)
    return jsonify(quest_dictionary)


@securityguideAPI.route(endpoint + "/priority_answers/email/<string:email>", \
                        methods=['POST', 'GET'])
def priority_questionnaire_answers(email):
    if request.method == 'POST':
        req = request.get_json()
        results_dicts_list = req['results']    
        db_manager.insert_priority_order(email, results_dicts_list)
        return jsonify("Custom priority order was submitted")
        
    else:
        subcategories_priority_order = {}
        try:
            user = auth_manager.retrieve_user_by_email(email)
            custom_priority_order_tmp = db_manager.get_priority_order(user['email'])
            tmp = custom_priority_order_tmp[0][0]
            tmp = tmp.replace("\'", "\"")
            subcategories_priority_order = \
            questionnaires_processor.compute_subcategories_priority_order(tmp)
            response = Response(json.dumps(subcategories_priority_order), \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response


"""------------------------ ORGANIZATION TYPE ------------------------------"""
@securityguideAPI.route(endpoint + "/organization_type/email/<string:email>", \
                        methods = ['POST', 'GET'])
def organization_type(email):  
    if request.method == 'POST':
        req = request.get_json()
        organization_type = req['organizationType']
        organization_type_dict = {}
        organization_type_dict['type'] = organization_type
        db_manager.insert_organization_type(email, organization_type_dict['type'])
        return jsonify('Organization type submitted')
    else:
        try:
            user = auth_manager.retrieve_user_by_email(email)
            organization_type = db_manager.get_organization_type(user['email'])
            organization_type = organization_type[0][0]
            organization_type_name = \
            recommendations_generator.get_organization_type_name(organization_type)
            response = Response(json.dumps(organization_type_name), \
                                mimetype='application/json', status=200)
        except Exception as e:
            response = handleException(e)
        finally:
            return response

"""------------------------- RECOMMENDATIONS -------------------------------"""
@securityguideAPI.route(endpoint + "/recommendations/email/<string:email>", methods = ['GET'])
def recommendations(email):
    recommendations_list = {}
    try:
        user = auth_manager.retrieve_user_by_email(email)
        organization_type = db_manager.get_organization_type(user['email'])
        organization_type_name = \
            recommendations_generator.get_organization_type_name(organization_type[0][0])  
        risk_answers_tmp = db_manager.get_risk_answers(user['email'])                 
        tmp = risk_answers_tmp[0][0]
        tmp = tmp.replace("\'", "\"")
        tmp2 = json.loads(tmp)
        risk_answers = tmp2['results']  
        recommendations_list = \
            recommendations_generator.generate_recommendations\
                (risk_answers, organization_type_name, email)
        
        for item in recommendations_list:
            item['practice'] = item['practice'].replace('\\n', '\n')
            item['evidence'] = item['evidence'].replace('\\n', '\n')  
        
        response = Response(json.dumps(recommendations_list), \
                            mimetype='application/json', status=200)
    except Exception as e:
        response = handleException(e)
    finally:
        return response

def handleException(e):
    result = json.dumps({"error": str(e)})
    print("=======================================" + result + "=======================================" )
    return Response(result, mimetype='application/json', status=500)

