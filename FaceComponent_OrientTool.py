import maya.cmds as maya
from functools import partial

#used for the face shared the same normals
windowID='normalSnap'

R_channel_keyable=False
T_channel_keyable=False
global duplicateMode
duplicateMode=False

def channeldetection():
	targetObj=maya.textScrollList(targetObjBox,q=True,si=True)[0]	
	if((not maya.getAttr(targetObj+'.translateX',l=True)) and (not maya.getAttr(targetObj+'.translateY',l=True)) and (not maya.getAttr(targetObj+'.translateZ',l=True))):
		print 'translation channel unlock!'
		key_translateX=maya.listConnections(targetObj+'.translateX',s=True,d=False)
		key_translateY=maya.listConnections(targetObj+'.translateY',s=True,d=False)
		key_translateZ=maya.listConnections(targetObj+'.translateZ',s=True,d=False)
		if(key_translateX or key_translateY or key_translateZ):
			print 'detect translation connection at the attribute channel'
			global T_channel_keyable
			T_channel_keyable=True
	else:
		maya.error('Found locked Rotation channel')

	if((not maya.getAttr(targetObj+'.rotateX',l=True)) and (not maya.getAttr(targetObj+'.rotateY',l=True)) and (not maya.getAttr(targetObj+'.rotateZ',l=True))):
		print 'rotation channel unlock!'
		key_RotateX=maya.listConnections(targetObj+'.rotateX',s=True,d=False)
		key_RotateY=maya.listConnections(targetObj+'.rotateY',s=True,d=False)
		key_RotateZ=maya.listConnections(targetObj+'.rotateZ',s=True,d=False)
		if(key_RotateX or key_RotateY or key_RotateZ):
			print 'detect rotation connection at the attribute channel'
			global R_channel_keyable
			R_channel_keyable=True
	else:
		maya.error('Found locked Rotation channel!!')

#expandFace and filter face Only
def processFaceSelection():
	selectface=maya.ls(sl=True)
	expandedFace=[]
	for face in selectface:
		if maya.filterExpand(face,sm=34)==None:
			return expandedFace
		else:
			for subface in maya.filterExpand(face,sm=34):
				expandedFace.append(subface)
	return expandedFace

def main():
	facecluster=[]
	dupobject=[]
	#return null if no target object specified
	if maya.textScrollList(targetObjBox,q=True,si=True)==None:
		return
	selectface=processFaceSelection()
	#if not select face, return null
	if selectface==None:
		return
	if maya.radioButtonGrp(snapModeButton,q=True,sl=True)==2:
		duplicateMode=True
		grp_dupObj=maya.group(n='grp_dup_transform',em=True)
	else:
		duplicateMode=False
	targetObj=maya.textScrollList(targetObjBox,q=True,si=True)[0]
	objectname=selectface[0].split('.')[0]
	#print objectname
	for com in selectface:
		#print com
		if duplicateMode==True:
			dup_targetObj=maya.duplicate(targetObj,n='dup_'+targetObj)
			maya.parent(dup_targetObj,grp_dupObj)
		dup_object=maya.duplicate(objectname,n='dup_'+objectname)
		dupobject.append(dup_object[0])
		#print dupobject			
		raw_data=maya.polyInfo(com,fv=True)[0]
		#print raw_data
		#data processing
		raw_verindex=raw_data.split(':')[1]
		#print raw_verindex
		verindex=[]  
		ver_all=raw_verindex.split(' ')
		#print ver_all
		for ver in ver_all:
			if ver != ''and ver != '\n':
				verindex.append(ver)
		#print verindex
		for ver in verindex:
			#print objectname
			cluster_temp=maya.cluster(objectname+'.vtx[{0}]'.format(ver),en=True,rel=True)
			if duplicateMode==True:
				maya.pointConstraint(cluster_temp,dup_targetObj,o=(0,0,0))
			else:			
				maya.pointConstraint(cluster_temp,targetObj,o=(0,0,0))
			facecluster.append(cluster_temp)
		#print facecluster
		maya.polyChipOff(dup_object[0]+'.'+com.split('.')[1],kft=True,dup=True,off=0,ch=True)
		grp_obj=maya.polySeparate(dup_object,o=True,n='seperate_'+dup_object[0])
		if duplicateMode==True:
			maya.normalConstraint(grp_obj[1],dup_targetObj,aim=(0,1,0),u=(1,0,0),wut='vector')
		else:
			maya.normalConstraint(grp_obj[1],targetObj,aim=(0,1,0),u=(1,0,0),wut='vector')


	#print T_channel_keyable
	#print R_channel_keyable
	if T_channel_keyable:
		maya.setKeyframe(targetObj,at='translataeX')
		maya.setKeyframe(targetObj,at='translateY')
		maya.setKeyframe(targetObj,at='translateZ')
		maya.delete(targetObj+'_pointConstraint*')
	  
	if R_channel_keyable:
		maya.setKeyframe(targetObj,at='rotateX')
		maya.setKeyframe(targetObj,at='rotateY')
		maya.setKeyframe(targetObj,at='rotateZ')	
		maya.delete(targetObj+'_normalConstraint*')
	#print facecluster
	for cluster in facecluster:
		#not sure here which to delete??
		maya.delete(cluster)
	for dupObj in dupobject:
		maya.delete(dupObj)

def normalSnap(*arg):
	#channeldetection()
	main()

def add_object(*arg):
	selectobj=maya.ls(sl=True,tr=True)
	if len(selectobj)==0:
		return
	exsitingobj=maya.textScrollList(targetObjBox,q=True,ai=True)
	if exsitingobj==None:
		exsitingobj=[]
	newobj=list(set(selectobj)-set(exsitingobj))
	maya.textScrollList(targetObjBox,e=True,a=newobj)
	#if no object selected
	if not maya.textScrollList(targetObjBox,q=True,si=True):
		maya.textScrollList(targetObjBox,e=True,si=newobj[0])

def remove_object(*arg):
	selectobj=maya.textScrollList(targetObjBox,q=True,si=True)
	print selectobj
	maya.textScrollList(targetObjBox,e=True,ri=selectobj)


def normalSnaPanel():	
	maya.window(windowID,widthHeight=(300,150),title='Normal Snap Tool',s=True,rtf=True)
	maya.columnLayout(w=300,h=150,rs=2)
	maya.text(l='Normal Snap Tool',al='center',w=300,fn='boldLabelFont')
	maya.columnLayout(cat=('left',50))
	global targetObjBox
	targetObjBox=maya.textScrollList(w=200,h=50)
	maya.columnLayout(h=10)
	maya.setParent('..')
	maya.rowLayout(nc=2,cat=(2,'left',20))
	maya.button(l='Add object',w=90,c=add_object)
	maya.button(l='Remove object',w=90,c=remove_object)
	maya.setParent('..')
	maya.columnLayout(h=10)
	maya.setParent('..')
	maya.setParent('..')
	#maya.rowLayout(nc=2,cat=(2,'left',0))
	maya.columnLayout()
	global snapModeButton
	snapModeButton=maya.radioButtonGrp(w=300,numberOfRadioButtons=2, l='Snap Mode:', labelArray2=[
                                         'Single','Duplicate'], cw3=[110,70,70],sl=1)	
	#global dupcheckBox
	#dupcheckBox=maya.checkBox(l='Duplicate',w=80)
	maya.setParent('..')
	maya.columnLayout(cat=('left',90))
	global snapbutton
	snapbutton=maya.button(l='SNAP!',w=120,bgc=[0.4,0.4,0.4],c=normalSnap)
	maya.showWindow(windowID)

def normalSnapGUI():
	if (maya.window(windowID,ex=True)):
		maya.deleteUI(windowID, wnd=True)
	normalSnaPanel()
	
normalSnapGUI()	






#normal caluculatation
'''print com
raw_data=maya.polyInfo(com,fn=True)[0]
print raw_data
#data processing
raw_normal=raw_data.split(':')[1]
print raw_normal
#print raw_normal
temp_normal=(float (raw_normal.split(' ')[1]),float (raw_normal.split(' ')[2]), float(raw_normal.split(' ')[3]))
print type(temp_normal[0])
normal.append(temp_normal)
print normal'''