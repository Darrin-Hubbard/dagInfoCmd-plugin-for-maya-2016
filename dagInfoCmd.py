# Copyright (C) 
# 
# Author: Autodesk Developer Network

#For this exercise, search for the TODO keywords and follow the instructions in
#comments. If you are unsure of what you need to do, feel free to ask the instructor
#or look into the solution folder.
#Each #... line is a line of code you need to write or complete.

import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

# Command name
kPluginCmdName = "dagInfoCmd"

# dagInfo command
class dagInfo(OpenMayaMPx.MPxCommand):
	
	def __init__(self):
		OpenMayaMPx.MPxCommand.__init__(self)

	#- This method performs the action of the command. It iterates over all
	#- selected items and prints out connected plug and dependency node type
	#- information.
	def doIt(self, args):
		#- Select all objects currently selected into the Maya editor.
		slist = OpenMaya.MSelectionList()
		OpenMaya.MGlobal.getActiveSelectionList( slist )
		#- Create an iterator on the selection list (using the iterator pattern).
		iter = OpenMaya.MItSelectionList( slist, OpenMaya.MFn.kDagNode )

		#- Iterate over all selected dependency nodes
		while ( iter.isDone() == 0 ): 
			#- Not getting the dag path, it will only return one path. I.e.:
			#dagPath = OpenMaya.MDagPath 
			#iter.getDagPath(dagPath)

			#- Instead, get the dependency node first and then apply MFnDagNode function set onto it.
			depNode = OpenMaya.MObject()
			iter.getDependNode(depNode)

			fnDag = OpenMaya.MFnDagNode(depNode)
			print "********************************************************"
			sys.stdout.write( '\n' )
			print "The selected node name is %s" % fnDag.name()
			print ", node type : %s" % depNode.apiTypeStr()
			sys.stdout.write( '\n' )

			#- TODO: Retrieve number of instances on this dag node
			num = fnDag.instanceCount(1)
			if( num != 1 ):
				print "Number of instances on this node is : %d" % num
				sys.stdout.write( '\n' )
			
			#Save out the MMatrix __str__ function so we can replace it once were done
			oldMMatrix_str = OpenMaya.MMatrix .__str__		
			# Call my new printing function to print the matrix so that is it readable
			OpenMaya.MMatrix.__str__ = myMatrix_str		
			
			#- TODO: Retrieve all the instanced paths of this dag node and print out them
			dagPathArray = OpenMaya.MDagPathArray()
			fnDag.getAllPaths(dagPathArray)
			for j in range (0, dagPathArray.length()):
				instanceDagPath = dagPathArray[j]
				#- TODO: Get this instance full dag path and print it
				print "Dag Path %d for this node: %s" % (j, instanceDagPath.fullPathName())
				
				sys.stdout.write( '\n' )
			
				#- TODO: Get the exclusive matrix of this node
				exMatrix = instanceDagPath.exclusiveMatrix()
				
				print "The exclusive transformation matrix of this node is "
				print exMatrix
				sys.stdout.write( '\n' )

				#- TODO: Get the inclusive matrix of this node
				#- If it is a shape node, the inclusive and exclusive matrix should be the same
				#- If it is a transform node and its transformation matrix is not identity, they 
				#- should be different!
				inMatrix = instanceDagPath.inclusiveMatrix()
				print "The inclusive transformation matrix of this node is "
				print inMatrix
				sys.stdout.write( '\n' )

				#- TODO: If this dag node is a transform node, also get its local transformation matrix
				if (depNode.hasFn(OpenMaya.MFn.kTransform)):
					fnTrans = OpenMaya.MFnTransform(instanceDagPath)
					localMatrix = fnTrans.transformation()
					print "The local transformation matrix represented by this transform node is "
					print localMatrix.asMatrix()
					sys.stdout.write( '\n' )

			iter.next()
			# Replace MMatrix __str__ function to the default
			OpenMaya.MMatrix.__str__ = oldMMatrix_str


#New __str__ function for Making the matrix readable....
def myMatrix_str(self):
	return "[[%g,%g,%g,%g][%g,%g,%g,%g][%g,%g,%g,%g][%g,%g,%g,%g]]" % (self(0,0), self(0,1), self(0,2), self(0,3), 
	self(1,0), self(1,1), self(1,2), self(1,3), self(2,0), self(2,1), self(2,2), self(2,3), self(3,0), self(3,1), self(3,2), self(3,3))

# Creator
def cmdCreator():
	return OpenMayaMPx.asMPxPtr( dagInfo() )

# Initialize the script plug-in
def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.registerCommand( kPluginCmdName, cmdCreator )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % kPluginCmdName )

# Uninitialize the script plug-in
def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterCommand( kPluginCmdName )
	except:
		sys.stderr.write( "Failed to unregister command: %s\n" % kPluginCmdName )

