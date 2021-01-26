from IDatasource import IDatasource
import rospy
from refills_perception_interface.knowrob_wrapper import KnowRob
from refills_perception_interface.tfwrapper import lookup_pose
from world_control_msgs.srv import SpawnModelRequest

#start test
import json
#end test

class KnowrobData(IDatasource):

    def __init__(self):
        #rospy.init_node("KnowRobCommunicatorNode")
        self.knowrob=KnowRob(initial_mongo_db=None, clear_roslog=False)
  
    def getAllShelfSystems(self, storeId):
        shelf_ids = self.knowrob.get_shelf_system_ids(False)
        shelvesSystem = []
        for shelf_id in shelf_ids:
            request = SpawnModelRequest()
            request.id = shelf_id.rsplit('#', 1)[1] # http://knowrob.org/kb/dm-market.owl#DMShelfW100_BRFNJTMX cut the url away
            shelf_pose = self.knowrob.get_shelf_pose(shelf_id)
            request.pose.position = shelf_pose.pose.position
            request.pose.orientation = shelf_pose.pose.orientation # Currently Shelves have more then one Type we will need the longest Typename which in the future will be the only one
            allTypesOfShelf = self.knowrob.all_solutions("has_type('{}', Type)".format(shelf_id))
            for TypeSet in allTypesOfShelf:
                biggestSet = ""
                if (len(biggestSet) < len(TypeSet)):
                    biggestSet = TypeSet
            modelPath = self.knowrob.once("subclass_of('{}', MeshDesc), has_description(MeshDesc, value(knowrob:pathToCadModel, FilePath))".format(biggestSet['Type']))['FilePath']  # Get the Meshname for spawning from the Meshpath
            modelName = modelPath.rsplit('/', 1)[1]  # split url at last / so Modelfilename is left
            if (modelName.startswith("SM_")):
                modelName = modelName[3:]
            request.name = modelName.rsplit('.', 1)[0]  # cut file ending
            shelvesSystem.append(request)


        return shelvesSystem

    def getAllShelfLayers(self,storeId):
        layer = []
        shelf_ids = self.knowrob.get_shelf_system_ids(False)
        for shelf_id in shelf_ids:

            layerDict = self.knowrob.get_shelf_layer_from_system(shelf_id)
            for shelfLayerId in layerDict:
                layerrequest = SpawnModelRequest()
                shelfLayerMapPose = lookup_pose('map', self.knowrob.get_object_frame_id(shelfLayerId)).pose
                shelfLayerTypes = self.knowrob.all_solutions("has_type('{}', Type)".format(shelfLayerId))
                for TypSet in shelfLayerTypes:
                    if (TypSet['Type'].rsplit('#', 1)[1].startswith("DM")):
                        interesstingType = TypSet['Type']
                shelfLayerModelPath = self.knowrob.once(
                    "subclass_of('{}', MeshDesc), has_description(MeshDesc, value(knowrob:pathToCadModel, FilePath))".format(
                        interesstingType))['FilePath']
                shelflayerModelName = shelfLayerModelPath.rsplit('/', 1)[
                    1]  # split url at last / so Modelfilename is left
                layerrequest.id = shelfLayerId.rsplit('#', 1)[1]
                layerrequest.name = shelflayerModelName.rsplit('.', 1)[0]  # cut file ending
                layerrequest.pose = shelfLayerMapPose
                layer.append(layerrequest)
        return layer

    def getStore(self, storeId):
        storeInterior=[]
        storeInterior.append(self.getAllShelves(storeId))
        storeInterior.append(self.getAllItems(storeId))
        return storeInterior

    def getAllShelves(self, storeId):
        shelf_ids = self.knowrob.get_shelf_system_ids(False)
        shelves = []
        for shelf_id in shelf_ids:
            request = SpawnModelRequest()
            request.id = shelf_id.rsplit('#', 1)[1] # http://knowrob.org/kb/dm-market.owl#DMShelfW100_BRFNJTMX cut the url away
            shelf_pose = self.knowrob.get_shelf_pose(shelf_id)
            request.pose.position = shelf_pose.pose.position
            request.pose.orientation = shelf_pose.pose.orientation # Currently Shelves have more then one Type we will need the longest Typename which in the future will be the only one
            allTypesOfShelf = self.knowrob.all_solutions("has_type('{}', Type)".format(shelf_id))
            for TypeSet in allTypesOfShelf:
                biggestSet = ""
                if (len(biggestSet) < len(TypeSet)):
                    biggestSet = TypeSet
            modelPath = self.knowrob.once("subclass_of('{}', MeshDesc), has_description(MeshDesc, value(knowrob:pathToCadModel, FilePath))".format(biggestSet['Type']))['FilePath']  # Get the Meshname for spawning from the Meshpath
            modelName = modelPath.rsplit('/', 1)[1]  # split url at last / so Modelfilename is left
            if (modelName.startswith("SM_")):
                modelName = modelName[3:]
            request.name = modelName.rsplit('.', 1)[0]  # cut file ending
            shelves.append(request)
#-------------------------------------------------------------------------
            layerDict = self.knowrob.get_shelf_layer_from_system(shelf_id)
            for shelfLayerId in layerDict:
                layerrequest = SpawnModelRequest()
                shelfLayerMapPose = lookup_pose('map', self.knowrob.get_object_frame_id(shelfLayerId)).pose
                shelfLayerTypes = self.knowrob.all_solutions("has_type('{}', Type)".format(shelfLayerId))
                for TypSet in shelfLayerTypes:
                    if (TypSet['Type'].rsplit('#', 1)[1].startswith("DM")):
                        interesstingType = TypSet['Type']
                shelfLayerModelPath = self.knowrob.once(
                    "subclass_of('{}', MeshDesc), has_description(MeshDesc, value(knowrob:pathToCadModel, FilePath))".format(
                        interesstingType))['FilePath']
                shelflayerModelName = shelfLayerModelPath.rsplit('/', 1)[
                    1]  # split url at last / so Modelfilename is left
                layerrequest.id = shelfLayerId.rsplit('#', 1)[1]
                layerrequest.name = shelflayerModelName.rsplit('.', 1)[0]  # cut file ending
                layerrequest.pose = shelfLayerMapPose
                shelves.append(layerrequest)
        return shelves

    #Hack -.-
    def getAllItems(self, storeId):
        items = []
        productDict = self.knowrob.all_solutions(
            "has_type(ItemId, ItemType), transitive(subclass_of(ItemType, shop:'Product'))")
        for product in productDict:
            itemModelPath = self.knowrob.once(
                "subclass_of('{}', MeshDesc), has_description(MeshDesc, value(knowrob:pathToCadModel, FilePath))".format(
                    product['ItemType']))['FilePath']
            itemModelName = itemModelPath.rsplit('/', 1)[1]
            itemrequsest = SpawnModelRequest()
            itemPoseMsg = self.knowrob.prolog_to_pose_msg(
                self.knowrob.once("is_at('{}', Pose)".format(product['ItemId']))['Pose'])
            itemrequsest.id = product['ItemId']
            itemrequsest.name = itemModelName.rsplit('.', 1)[0]
            itemrequsest.pose = lookup_pose('map', self.knowrob.get_object_frame_id(product['ItemId'])).pose
            items.append(itemrequsest)
        return items
        # calcualate Pose dependent on Layer -- Find where the Frame is --> Messy



    def spawnModulMsgToJson(self, inMessage):
        print(10*'%')
        print(inMessage)
        jsonMessage=\
            {
                'name': inMessage.name.encode('ascii'),
                'pose':
                {
                    'position':
                    {
                        'x': inMessage.pose.position.x,
                        'y': inMessage.pose.position.y,
                        'z': inMessage.pose.position.z
                    },
                    'orientation':
                    {
                        'x': inMessage.pose.orientation.x,
                        'y': inMessage.pose.orientation.y,
                        'z': inMessage.pose.orientation.z,
                        'w': inMessage.pose.orientation.w
                    }

                },
                'id': inMessage.id.encode('ascii'),
                'tags':inMessage.tags,
                'path': inMessage.path,
                'actor_label': inMessage.actor_label,
                'physics_properties':
                {
                    'mobility': inMessage.physics_properties.mobility,
                    'gravity': inMessage.physics_properties.gravity,
                    'generate_overlap_events': inMessage.physics_properties.generate_overlap_events,
                    'mass': inMessage.physics_properties.mass
                },
                'material_names': inMessage.material_names,
                'material_paths': inMessage.material_paths,
                'parent_id': inMessage.parent_id
            }
        return json.dumps(jsonMessage) #finally returns a correct JSONMessage

    def getAllShelfSystemsJSON(self,storeId):
        shelfdata=self.getAllShelfSystems(1)
        shelfsystemJson=[]
        for data in shelfdata:
            shelfsystemJson.append(self.spawnModulMsgToJson(data))

        return json.dumps(shelfsystemJson)


    def getAllShelfLayersJSON(self,storeId):
        shelfdata=self.getAllShelfLayers(storeId)
        layersjson=[]
        for data in shelfdata:
            layersjson.append(self.spawnModulMsgToJson(data))

        return json.dumps(layersjson)

    def getAllShelvesJSON(self,storeId):
        shelfdata=self.getAllShelves(storeId)
        shelfjson=[]
        for data in shelfdata:
            shelfjson.append(self.spawnModulMsgToJson(data))

        return json.dumps(shelfjson)

    def getAllItemsJSON(self,storeId):
        itemdata=self.getAllItems(storeId)
        itemJson=[]
        for data in itemdata:
            itemJson.append(self.spawnModulMsgToJson(data))

        return json.dumps(itemJson)

    def getStoreJSON(self,storeId):
        storeData=self.getStore(storeId)
        storeJson=[]
        for data in storeData:
            storeJson.append(self.spawnModulMsgToJson(data))

        return json.dumps(storeJson)

    def getSortedStoreJSON(self,storeId):
        systemData=self.getAllShelfSystems(storeId)
        system=[]
        layerData=self.getAllShelfLayers(storeId)
        layer=[]
        itemData=self.getAllItems(storeId)
        item=[]
        storeJson={}
        for data in systemData:
            system.append(self.spawnModulMsgToJson(data))

        for data in systemData:
            system.append(self.spawnModulMsgToJson(data))
        for data in layerData:
            layer.append(self.spawnModulMsgToJson(data))
        for data in itemData:
            item.append(self.spawnModulMsgToJson(data))

        storeJson["shelfsystems"]=system
        storeJson["shelfLayer"]=layer
        storeJson["items"]=item

        return json.dumps(storeJson)

