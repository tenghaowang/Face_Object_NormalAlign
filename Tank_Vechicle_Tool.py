import maya.cmds as maya
windowID='mywindow'
constraintground=False
children=[]
cl_l_tread='grp_cl_l_treadwheel01'
cl_r_tread='grp_cl_r_treadwheel01'
buttonlabel='Constraint to Ground'
label_constraint='Constraint to Ground'
label_Unconstraint='Unconstraint to Ground'

def riggingpanel():	
	maya.window(windowID,widthHeight=(500,500),title='Vechicles\Tank Tool',s=False)
	myform=maya.formLayout()
	layout=maya.columnLayout(cat=['both',50],rs=10,columnWidth=500)
	maya.text(l='Tank Rigging/Support Tool',al='center',w=300,h=20,fn='boldLabelFont')
	maya.text(l='please select the terrain and constrain the tank to ground',fn='boldLabelFont',h=20,al='center')
	global children
	children=cmds.listRelatives(cl_l_tread,cl_r_tread,c=True)
	for child in children:
		if maya.objExists(child+'_geometryConstraint*'):
			global constraintground
			constraintground=not constraintground
			global buttonlabel
			buttonlabel=label_Unconstraint
			break
	global constraintbutton
	constraintbutton=maya.button(p=layout,w=200,h=50,l=buttonlabel,c=constraintButton_Pressed)
	maya.text(l='helps to fast reset all the treads controls position',fn='boldLabelFont',h=20,al='center')
	maya.text(l='works only when the tank is not constraint to ground',fn='boldLabelFont',h=20,al='center')
	resetbutton=maya.button(p=layout,w=200,h=50,l='reset all the treads position',c=resetbutton_Pressed)
	maya.text(l='align the Vechicle to the surface',fn='boldLabelFont',h=20,al='center')
	alignbutton=maya.button(p=layout,w=200,h=50,l='normal alignment',c=alignbutton_Pressed)
	cmds.formLayout(myform,e=True,attachForm=[(layout,'top',30),(layout,'left',10),(layout,'right',10),(layout,'bottom',10)])
	#print constraintbutton
	maya.showWindow(windowID)
def alignbutton_Pressed(* arg):
	print '1'
def resetbutton_Pressed(* arg):
	global constraintground
	if not constraintground:
		print 'reset the treads'
		global children
		for child in children:
			maya.setAttr(child+'.translate',0,0,0)
	else:
		maya.warning('the tank is constraint to the ground!')
def constraintButton_Pressed(* arg):
	global constraintground
	constraintground=not constraintground
	print constraintground
	if(constraintground):
		maya.button(constraintbutton,e=True,l='UnConstraint to Ground')
		terrain=maya.ls(sl=True)
		if not terrain:
			maya.warning('please select a ground')
		#if len(terrain)>1:
			#maya.warning('please select one ground only')
		else:
			#for tank rigging only:
			for child in children:
				print child
				maya.geometryConstraint(terrain[0],child,w=1)
	else:
		maya.button(constraintbutton,e=True,l='Constraint to Ground')
		for child in children:
			if maya.objExists(child+'_geometryConstraint*'):
				maya.delete(child+'_geometryConstraint*')


def rigginggui():
	if (maya.window(windowID,ex=True)):
		maya.deleteUI(windowID, wnd=True)
	riggingpanel()
	
rigginggui()	