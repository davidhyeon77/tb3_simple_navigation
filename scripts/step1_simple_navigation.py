#!/usr/bin/env python
# license removed for brevity

import rospy
import actionlib
import rosmaster.master_api
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

destination1 = [[0.7, -1.6, 0.0]]
destination2 = [[0.0, 0.0, 0.0]]
orientation = (0.0, 0.0, 0.0, 1.0)

# Turtlebot3 Specification
LIN_SPEED =  0.1

# set parking zone(kind of tolerlance)
DIST = 0.15

def movebase_client(dest, orient):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = dest[0]
    goal.target_pose.pose.position.y = dest[1]
    goal.target_pose.pose.position.z = dest[2]
    goal.target_pose.pose.orientation.x = orient[0]
    goal.target_pose.pose.orientation.y = orient[1]
    goal.target_pose.pose.orientation.z = orient[2]
    goal.target_pose.pose.orientation.w = orient[3]

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
        
def straight(self):
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)

    tw = Twist()
    tw.linear.x = - LIN_SPEED
    pub.publish(tw)
    
    duration = DIST / LIN_SPEED
    time2end = rospy.Time.now() + rospy.Duration(duration)
    
    while time2end > rospy.Time.now():
        pass

    
    tw.linear.x = 0
    pub.publish(tw)

if __name__ == '__main__':
    try:
        rospy.init_node('movebase_client_py')

        arrive = rospy.get_param("/step1_nav_arrive/nav_arrive_end") 
        target = rospy.get_param("/step1_nav_arrive/target")
        
        if arrive == False:
            if target == 1:
                i = 0
                while i < 1:
                    movebase_client(destination1[i], orientation) 
                    i = i + 1
                
                rospy.set_param("/step1_nav_arrive/nav_arrive_end", True)    
            
            elif target == 2:    
                straight()
                               
                i = 0
                while i < 1:
                    movebase_client(destination2[i], orientation) 
                    i = i + 1
        
                rospy.set_param("/step1_nav_arrive/nav_arrive_end", True)       
                 
            rospy.loginfo("Goal execution done!")
            
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
