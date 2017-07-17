from flask import Flask
from flask import request
from tracker import Tracker
import sys
import os
import traceback
import json
from complexencoder import ComplexEncoder

app = Flask(__name__)

# Setup subscribers
goals_tracker = Tracker.build_new_tracker();

@app.route("/test")
def hello():
    return "Hello World!"

def serialize_response(object):
    if type(object) == list:
        return json.dumps([o.toJSON() for o in object])
    else:
        #print "[serialize_object] Object: ", json.dumps(object.__dict__)
        if hasattr(object, 'toJSON'): 
            return json.dumps(object.toJSON())
        elif type(object) == str:
            return json.dumps(object)
        else:
            return json.dumps(object.__dict__)

################################ GOALS ############################################
@app.route("/goaltracker/goals/put/<goalname>", methods=['GET','POST'])
def put_goal(goalname):
    print "Put goal:", goalname
    return serialize_response(goals_tracker.put_goal(goalname))

@app.route("/goaltracker/goals/delete/<goalname>", methods=['GET','POST'])
def delete_goal(goalname):
    print "Delete goal:", goalname
    return serialize_response(goals_tracker.delete_goal(goalname))

@app.route("/goaltracker/goals/get/<goalname>", methods=['GET'])
def get_goal(goalname):
    print "Get goal:", goalname
    return serialize_response(goals_tracker.get_goals(goalname))

@app.route("/goaltracker/goals/<goalname>/put/steps/<stepname>/estimate/<int:estimate>", methods=['GET','POST'])
def put_goal_step(goalname, stepname, estimate):
    return serialize_response(goals_tracker.put_step(goalname, stepname, estimate))

@app.route("/goaltracker/goals/<goalname>/get/steps", methods=['GET','POST'])
def get_goal_steps( goalname):
    return serialize_response(goals_tracker.get_steps(goalname))

@app.route("/goaltracker/goals/<goalname>/markcomplete/steps/<stepname>", methods=['GET','POST'])
def mark_step_complete(goalname, stepname):
    return serialize_response(goals_tracker.mark_step_complete(goalname, stepname))

@app.route("/goaltracker/goals/<goalname>/markincomplete/steps/<stepname>", methods=['GET','POST'])
def mark_step_incomplete( goalname, stepname):
    return serialize_response(goals_tracker.mark_step_incomplete(goalname, stepname))
###################################################################################
