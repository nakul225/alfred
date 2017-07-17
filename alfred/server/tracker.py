import sys
import pickle
import os
import traceback
from goal import Goal
from step import Step
import json
from complexencoder import ComplexEncoder

class Tracker:       
    def __init__(self):
        self.categories = []
        self.goals = []

    def toJSON(self):
        return json.dumps(self.__dict__, cls=ComplexEncoder)

    def _get_tracker_file(self):
        return "./user.data"

    def _write_to_datastore(self):
        # Save goal data to a file
        with open(self._get_tracker_file(), 'wb') as f:
            pickle.dump(self, f)

    def _load_from_datastore(self):
        # read data from file
        # If files don't exist, return empty list
        try:
            with open(self._get_tracker_file(), 'rb') as f:
                return_value = pickle.load(f)
                self.categories = return_value.categories
                self.goals = return_value.goals
        except:
            print "Exception reading user data file: ", self._get_tracker_file()," exception: ", sys.exc_info()[0]
            self.categories = []
            self.goals = []

    def put_goal(self, goalname):
        goal_exists = self._search_goal(goalname)
        if goal_exists:
            message = "Goal already exists, won't create a new one"
            print message
            return message
        else:
            goal = Goal.build_new_goal(goalname, "")
            self.goals.append(goal)
            # persist
            self._write_to_datastore()
            return "Created goal" 

    def delete_goal(self, goalname):
        for g in self.goals:
            if g.name == goalname:
                self.goals.remove(g)
                # persist
                self._write_to_datastore()
                return "Goal deleted"
        return "Goal not found"

    def get_goals(self, goalname):
        self._load_from_datastore()

        if goalname == "*":
            return self.goals
        else:
            for g in self.goals:
                if g.name == goalname:
                    print "[INFO] Found goal: ", g," with the input name: ", goalname
                    return g
            print "[WARN] Did not find any goal with name: ", goalname
            return "No goal with given name found"

    def put_step(self, goalname, stepname, estimate):
        self._load_from_datastore()
        print "[INFO] put_step, goalname,stepname,estimate:", goalname, stepname, estimate
        print self.goals
        for goal in self.goals:
            if goalname == goal.name:
                # Modify the goal
                goal.put_step( Step.build_new_step(stepname, "", estimate) )
                #persist
                self._write_to_datastore() 
                return goal
        return "No goal with given name: ", goalname, " found."

    def get_steps(self, goalname):
        self._load_from_datastore()

        for g in self.goals:
            if g.name == goalname:
                return g.get_steps()
        return "No goal with given name: ", goalname, " found."

    def mark_step_complete(self, goalname, stepname):
        goal = self.get_goals(goalname)
        goal.mark_step_complete(stepname)
        self._write_to_datastore()
        return "Updated Goal"

    def mark_step_incomplete(self, goalname, stepname):
        goal = self.get_goals(goalname)
        goal.mark_step_incomplete(stepname)
        self._write_to_datastore()
        return "Updated Goal"

    def _get_total_num_of_goals(self):
        self._load_from_datastore()
        return len(self.goals)

    def _search_goal(self, goalname):
        self._load_from_datastore()
        print "_search_goal: ", self.goals
        for g in self.goals:
            if g.name == goalname:
                return True
        return False

    @staticmethod
    def build_new_tracker():
        return Tracker()
