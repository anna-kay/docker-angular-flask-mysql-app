import mysql.connector as mySQL
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

class DBManager:

    def getDatabaseConnection(self):
        return mySQL.connect(host=config['database']['host'], \
                             user=config['database']['user'], \
                             password=config['database']['password'], \
                             database=config['database']['database'])

    def get_recommendations_df(self):
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            select_query = "SELECT * FROM risk_recommendations"
            cursor.execute(select_query)
            recommendations_list = cursor.fetchall()
            recommendations_df = pd.DataFrame(recommendations_list,
                                          columns=['ID', 
                                                   'practice', 
                                                   'evidence', 
                                                   'security_domain_ID', 
                                                   'security_measure_ID',
                                                   'specialization_level',
                                                   'security_function',
                                                   'layer'
                                                   ])
            recommendations_df['type']='risk'
        except Exception as e:
            print("====================" + str(e) + "====================")
            recommendations_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
        return recommendations_df



    def get_security_domains_df(self):
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            select_query = "SELECT * FROM security_domains"
            cursor.execute(select_query)
            security_domains_list = cursor.fetchall()
            security_domains_df = pd.DataFrame(security_domains_list,
                                          columns=['ID', 
                                                   'name', 
                                                   'color'
                                                   ])
        except Exception as e:
            print("====================" + str(e) + "====================")
            security_domains_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
            return security_domains_df


    def get_security_measures_df(self):
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            select_query = "SELECT * FROM security_measures"
            cursor.execute(select_query)
            security_measures_list = cursor.fetchall()
            security_measures_df = pd.DataFrame(security_measures_list,
                                  columns=['ID', 
                                           'name', 
                                           'security_domain_ID'
                                           ])
        except Exception as e:
            print("====================" + str(e) + "====================")
            security_measures_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
            return security_measures_df


    def get_risk_subcategories_df(self):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            select_query = "SELECT * FROM risk_subcategories"
            cursor.execute(select_query)
            risk_subcategories_list = cursor.fetchall()
            risk_subcategories_df = pd.DataFrame(risk_subcategories_list,
                                  columns=['ID', 
                                           'subcategory', 
                                           'category', 
                                           'security_function', 
                                           'protocol_layer',
                                           'recommendations_ids',
                                           'maturity_recommendations_ids'
                                           ])
        except Exception as e:
            print("====================" + str(e) + "====================")
            risk_subcategories_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
            return risk_subcategories_df
    
    def get_maturity_recommendations_df(self):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            select_query = "SELECT * FROM maturity_recommendations"
            cursor.execute(select_query)
            maturity_recommendations_list = cursor.fetchall()
            maturity_recommendations_df = pd.DataFrame(maturity_recommendations_list,
                                  columns=['indicator',
                                           'maturity_recommendation',
                                           'SPEAR_subcategory',
                                           'maturity_category',
                                           'maturity_level'
                                           ])
            
            maturity_recommendations_df['type']='maturity'
        except Exception as e:
            print("====================" + str(e) + "====================")
            maturity_recommendations_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
            return maturity_recommendations_df
    
    
    def get_maturity_indicators_df(self):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            select_query = "SELECT * FROM maturity_levels_indicators"
            cursor.execute(select_query)
            maturity_indicators_list = cursor.fetchall()
            maturity_indicators_df = pd.DataFrame(maturity_indicators_list,
                                  columns=['maturity_level', 
                                            'category', 
                                            'indicators'])
        except Exception as e:
            print("====================" + str(e) + "====================")
            maturity_indicators_df = pd.DataFrame()
        finally:
            cursor.close()
            mydb.close()
            return maturity_indicators_df
    
        
    def insert_maturity_answers(self, email, answers):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO maturity_answers (email, answers) VALUES (%s, %s)"
            values = (email, str(answers))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success
    
    def get_maturity_answers(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            cursor.execute("SELECT answers FROM maturity_answers WHERE date=( SELECT max(date) FROM maturity_answers WHERE email = \'" + str(email) + "')")
            maturity_results = cursor.fetchall()
        except Exception as e:
            print("====================" + str(e) + "====================")
            maturity_results = []
        finally:
            cursor.close()
            mydb.close()
            return maturity_results
        
    def insert_maturity_targets(self, email, targets):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO maturity_targets (email, targets) VALUES (%s, %s)"
            values = (email, str(targets))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success 
    
    
    def get_maturity_targets(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            cursor.execute("SELECT targets FROM maturity_targets WHERE date=( SELECT max(date) FROM maturity_targets WHERE email = \'" + str(email) + "')")
            maturity_results = cursor.fetchall()
        except Exception as e:
            print("====================" + str(e) + "====================")
            maturity_results = []
        finally:
            cursor.close()
            mydb.close()
            return maturity_results


    def insert_risk_answers(self, email, answers):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO risk_answers (email, answers) VALUES (%s, %s)"
            values = (email, str(answers))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success
    
    
    def get_risk_answers(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            cursor.execute("SELECT answers FROM risk_answers WHERE date=( SELECT max(date) FROM risk_answers WHERE email = \'" + str(email) + "')")
            risk_results = cursor.fetchall()
        except Exception as e:
            print("====================" + str(e) + "====================")
            risk_results = []
        finally:
            cursor.close()
            mydb.close()
            return risk_results
        
        
    def insert_risk_targets(self, email, targets):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO risk_targets (email, targets) VALUES (%s, %s)"
            values = (email, str(targets))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("==================== insert_risk_targets ====================")
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success 
    
    
    def get_risk_targets(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            cursor.execute("SELECT targets FROM risk_targets WHERE date=( SELECT max(date) FROM risk_targets WHERE email = \'" + str(email) + "')")
            risk_results = cursor.fetchall()
        except Exception as e:
            print("==================== get_risk_targets ====================")
            print("====================" + str(e) + "====================")
            risk_results = []
        finally:
            cursor.close()
            mydb.close()
            return risk_results
    
    def insert_organization_type(self, email, organization_type):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO organization_type (email, organization_type) VALUES (%s, %s)"
            values = (email, str(organization_type))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success 

    def get_organization_type(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            # cursor.execute("SELECT targets FROM maturity_targets WHERE email = \'" + str(email) + "' AND MAX(date)")
            cursor.execute("SELECT organization_type FROM organization_type WHERE date=( SELECT max(date) FROM organization_type WHERE email = \'" + str(email) + "')")
            organization_type = cursor.fetchall()

        except Exception as e:
            print("====================" + str(e) + "====================")
            organization_type = []
        finally:
            cursor.close()
            mydb.close()
            return organization_type


    def insert_priority_order(self, email, custom_priority_order):
        success = False
        try:
            mydb = self.getDatabaseConnection()
            cursor = mydb.cursor()
            sql = "INSERT INTO priority_order (email, custom_priority_order) VALUES (%s, %s)"
            values = (email, str(custom_priority_order))
            cursor.execute(sql, values)
            mydb.commit()
            success = True
        except Exception as e:
            success = False
            print("====================" + str(e) + "====================")
        finally:
            cursor.close()
            mydb.close() 
            return success 

    def get_priority_order(self, email):
        mydb = self.getDatabaseConnection()
        cursor = mydb.cursor()
        try:
            # cursor.execute("SELECT targets FROM maturity_targets WHERE email = \'" + str(email) + "' AND MAX(date)")
            cursor.execute("SELECT custom_priority_order FROM priority_order WHERE date=( SELECT max(date) FROM priority_order WHERE email = \'" + str(email) + "')")
            custom_priority_order = cursor.fetchall()

        except Exception as e:
            print("====================" + str(e) + "====================")
            custom_priority_order = []
        finally:
            cursor.close()
            mydb.close()
            return custom_priority_order

