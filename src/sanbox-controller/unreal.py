from ICommunication import ICommunication
from world_control_msgs.srv import SpawnModel, SpawnModelRequest,SpawnModelResponse
import rospy

class Unreal(ICommunication):
    def __init__(self,inXOffset=0,inYOffset=0,inZOffset=0,intopicName="pie_rwc/spawn_model"):
        #rospy.init_node("Unreal")
        self._X_OFFSET=inXOffset
        self._Y_OFFSET=inYOffset
        self._Z_OFFSET=inZOffset
        self._topicName=intopicName

    def send(self,inList):
        print("Begin sending Messages. Spawning {} Items.".format(len(inList)))

        #assumption: inList is already in the correct format
        try:
            i=0
            for request in inList:
                spawnModelHandler = rospy.ServiceProxy(self._topicName, SpawnModel)
                request.pose.position.x -= self._X_OFFSET
                request.pose.position.y -= self._Y_OFFSET
                request.pose.position.z -= self._Z_OFFSET
                request.physics_properties.mobility = 0  # ToDo: Get an actual value here
                response = spawnModelHandler(request)
                print(response)
                # Todo:Add QuaterionOffset --> TFLookup?
                # request.pose.orientation -= self._OFFSET.Quaternion
                # request.pose.orientation.x -= self._OFFSET.Quaternion.x
                # request.pose.orientation.y -= self._OFFSET.Quaternion.y
                # request.pose.orientation.z -= self._OFFSET.Quaternion.z
        except rospy.ServiceException as e:
            print("Service call failed: {} ".format(e))
            return False
        print("Finish sending Messages")
        return True

