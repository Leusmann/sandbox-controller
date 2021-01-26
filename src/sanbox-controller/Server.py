#!/usr/bin/python -u
from flask import Flask
from knowrobData import KnowrobData
from unreal import Unreal
import rospy


#start test
import json
#end test

app=Flask(__name__)


@app.route('/')
def index():
    return "Hello World :)"

@app.route('/knowrob/api/v1.0/allData',methods=['GET'])
def get_allData():
    #response=datasouce.getSortedStoreJSON(1)
    response = datasouce.getStoreJSON(1) #? 
    return response

@app.route('/knowrob/api/v1.0/allSystems',methods=['GET'])
def get_allSystems():
    response=datasouce.getAllShelfSystemsJSON(1)
    return response

@app.route('/knowrob/api/v1.0/allLayers',methods=['GET'])
def get_allLayers():
    response=datasouce.getAllShelfLayersJSON(1)
    return response

@app.route('/knowrob/api/v1.0/allShelves',methods=['GET'])
def get_allShelves():
    response=datasouce.getAllShelvesJSON(1)
    return response


@app.route('/knowrob/api/v1.0/allItems',methods=['GET'])
def get_allItems():
    response=datasouce.getAllItemsJSON(1)
    return response


@app.route('/unreal/api/v1.0/spawnRealogram',methods=['GET'])
def get_spawnRealogram():
    shelfdata=datasouce.getAllShelves(1)
    itemdata=datasouce.getAllItems(1)
    app.logger.info("Gathered all the data will start spawning now")
    refills.send(shelfdata)
    refills.send(itemdata)
    return "True"

@app.route('/log/hello',methods=['GET'])
def get_logHello():
    print("Hello")
    app.logger.info("Hello from the Infor Log")
    return "True"



if __name__=='__main__':
    rospy.init_node("SandboxController")
    datasouce = KnowrobData()
    refills=Unreal(-3.1,-4.72,0) #refills X=-3.10,Y=-4.72, Z=0
    app.run(host='0.0.0.0',debug=True,port=62226)

