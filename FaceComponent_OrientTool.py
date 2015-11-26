import maya.cmds as maya
from functools import partial

#used for the face shared the same normals
windowID='normalSnap'
#component=maya.ls(sl=True)
normal=[]
facecluster=[]
#objectname=component[0].split('.')[0]
#dup_object=maya.duplicate(objectname,n='dup_'+objectname)
#targetobj=component[-1]
R_channel_keyable=False
T_channel_keyable=False
#for com in component:
	#if(maya.objectType(com,i='transform')):
		#targetobj=com
def channeldetection():
	if((not maya.getAttr(targetobj+'.translateX',l=True)) and (not maya.getAttr(targetobj+'.translateY',l=True)) and (not maya.getAttr(targetobj+'.translateZ',l=True))):
		print 'translation channel unlock!'
		key_translateX=maya.listConnections(targetobj+'.translateX',s=True,d=False)
		key_translateY=maya.listConnections(targetobj+'.translateY',s=True,d=False)
		key_translateZ=maya.listConnections(targetobj+'.translateZ',s=True,d=False)
		if(key_translateX or key_translateY or key_translateZ):
			print 'detect translation connection at the attribute channel'
			global T_channel_keyable
			T_channel_keyable=True
	else:
		maya.error('Found locked Rotation channel')

	if((not maya.getAttr(targetobj+'.rotateX',l=True)) and (not maya.getAttr(targetobj+'.rotateY',l=True)) and (not maya.getAttr(targetobj+'.rotateZ',l=True))):
		print 'rotation channel unlock!'
		key_RotateX=maya.listConnections(targetobj+'.rotateX',s=True,d=False)
		key_RotateY=maya.listConnections(targetobj+'.rotateY',s=True,d=False)
		key_RotateZ=maya.listConnections(targetobj+'.rotateZ',s=True,d=False)
		if(key_RotateX or key_RotateY or key_RotateZ):
			print 'detect rotation connection at the attribute channel'
			global R_channel_keyable
			R_channel_keyable=True
	else:
		maya.error('Found locked Rotation channel!!')


def main():
	for com in component:
		if(maya.objectType(com,i='mesh')):
			raw_data=maya.polyInfo(com,fv=True)[0]
			print raw_data
			#data processing
			raw_verindex=raw_data.split(':')[1]
			#print raw_verindex
			verindex=[]  
			ver_all=raw_verindex.split(' ')
			print '1'
			#print ver_all
			for ver in ver_all:
				if ver != ''and ver != '\n':
					verindex.append(ver)
			for ver in verindex:
				cluster_temp=maya.cluster(objectname+'.vtx[{0}]'.format(ver),en=True,rel=True)
				maya.pointConstraint(cluster_temp,targetobj,o=(0,0,0))
				facecluster.append(cluster_temp)
			print facecluster
			print dup_object[0]+com.split('.')[1]
			maya.polyChipOff(dup_object[0]+'.'+com.split('.')[1],kft=True,dup=True,off=0,ch=True)
			grp_obj=maya.polySeparate(dup_object,o=True,n='seperate_'+dup_object[0])
			print grp_obj
			maya.normalConstraint(grp_obj[1],targetobj,aim=(0,1,0),u=(0,1,0),wut='vector')


def normalSnap(*arg):
	channeldetection()
	main()
			#print targetobj
	#position constraint the targetobj
	print T_channel_keyable
	print R_channel_keyable
	if T_channel_keyable:
		maya.setKeyframe(targetobj,at='translataeX')
		maya.setKeyframe(targetobj,at='translateY')
		maya.setKeyframe(targetobj,at='translateZ')
		maya.delete(targetobj+'_pointConstraint*')
	  
	if R_channel_keyable:
		maya.setKeyframe(targetobj,at='rotateX')
		maya.setKeyframe(targetobj,at='rotateY')
		maya.setKeyframe(targetobj,at='rotateZ')	
		maya.delete(targetobj+'_normalConstraint*')

	for cluster in facecluster:
		maya.delete(cluster)
	maya.delete(dup_object)

def add_object(*arg):
	selectobj=maya.ls(sl=True)
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
	maya.window(windowID,widthHeight=(300,250),title='Normal Snap Tool',s=True,rtf=True)
	maya.columnLayout(w=300,h=250,rs=2)
	maya.text(l='Normal Snap Tool',al='center',w=300,fn='boldLabelFont')
	maya.columnLayout(cat=('left',50))
	global targetObjBox
	targetObjBox=maya.textScrollList(w=200,h=50)
	maya.columnLayout(h=10)
	maya.setParent('..')
	maya.rowLayout(nc=2,cat=(2,'left',20))
	maya.button(l='Add object',w=90,c=add_object)
	maya.button(l='Remove object',w=90,c=remove_object)
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