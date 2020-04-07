###########################
# SCRIPT MADE BY MP
# YOUTUBE https://www.youtube.com/channel/UCXvI8JRMsskPQrpQoSLeeBA
# DISCORD MP#9395
# STEAM https://steamcommunity.com/id/mov1Lgglrpower/
# GITHUB https://github.com/mpsterprod/
###########################
import os
import shutil
import maya.cmds as mc
from maya import mel

def Cod_Models_builder():
	# check mesh
	chh = mc.ls(type='mesh',s=0)
	if chh is None or chh==[]:
		print("no mesh. please import skeletal Mesh. for only joint don't work")
		return

	#return
	value_j = []
	for x in mc.ls(type='joint'):
		if x.find("|")!=-1:
			value_j.append(x)
			
	null_j = []
	vall = []

	for i in value_j:
		if i.find("j_gun")!=-1:
			if len(mc.ls(i,dagObjects=1))==1:
				mc.delete(i)
		else:
			# check skin cluster 
			ds = mc.listConnections(i)
			if ds == [] or ds is None:
				vall.append(i)
				continue
			nex_t = False
			for objff in ds:
				if mc.nodeType(objff)=="dagPose" or mc.nodeType(objff)=="skinCluster":
					null_j.append(i)
					nex_t = True
					break
			if nex_t:
				continue

			if mc.getAttr(i + '.translateX')==0 and mc.getAttr(i + '.translateY')==0 and mc.getAttr(i + '.translateZ')==0:
				if len(mc.ls(i,dagObjects=1))>1:
					# add mesh
					null_j.append(i)
			else:
				# add null
				vall.append(i)
	parents = dict()
	for pos_j in vall:		
		name = pos_j.replace("|",' ').split()
		for weight_j  in null_j:
			dsdsd = weight_j.replace("|",' ').split()
			if name[len(name)-1]==dsdsd[len(dsdsd)-1]:
				mc.matchTransform(weight_j,pos_j)
				parents[name[len(name)-1]] = mc.listRelatives(pos_j,parent=1)
				mc.delete(pos_j)
	for x in parents:
		mc.parent(x,parents[x][0])

	for jr in mc.ls(type='joint'):
		if jr.find("_weight")!=-1:
			mc.rename(jr,jr.replace("_weight",""))
	del null_j, vall

	

	# DELETE OTHER "Joints" transfroms objects
	root_grp_j = ''
	for tfm in mc.ls(type='transform'):
		if tfm.find("Joints")!=-1:
			if len(mc.ls(tfm,dagObjects=1))>1:
				root_grp_j = tfm
			else:
				mc.delete(tfm)
	fr_rename = False
	for rename_int in mc.ls(type='joint'):
		if rename_int == root_grp_j:
			fr_rename = True
			break
	if fr_rename:
		mc.rename(root_grp_j,root_grp_j[:len(root_grp_j)-1])

	# MESH GROUP
	all_transform = mc.ls(type='transform',allPaths=1)   # only work groups when there are all groups with meshes
	temp_transform = []
	for x in all_transform:
		if not mc.objectType(x)=='joint':
			if mc.listRelatives(x,type='mesh',shapes=0) is None:
				if mc.listRelatives(x,type='camera',shapes=0) is None:
					temp_transform.append(x)
	final_temp = []
	for x in temp_transform:
		# check joints grp
		if mc.ls(x,dagObjects=1) is not None:
			jont_t = True
			for dddddd in mc.ls(x,dagObjects=1):
				if mc.objectType(dddddd)=='joint':
					jont_t = False
					break
			if jont_t:
				final_temp.append(x)
	
	del temp_transform

	void_ts = ''
	for_parent = []
	for x in final_temp:
		if len(mc.ls(x,dagObjects=1))>1:
			for_parent.append(x)
		else:
			void_ts = x
	for root_grp in for_parent:
		# check in scene
		chl = False
		prn = False
		for j_cc in mc.ls(type='joint'):
			if root_grp==j_cc:
				chl = True
				break
		for j_PS in mc.ls(type='joint'):
			if root_grp==j_PS:
				prn = True
				break
		if chl and prn:
			mc.parent(root_grp,void_ts)
	del for_parent, void_ts, final_temp, root_grp, all_transform, parents

Cod_Models_builder()
