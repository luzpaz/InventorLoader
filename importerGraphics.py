# -*- coding: utf-8 -*-

'''
importerGraphics.py:
Simple approach to read/analyse Autodesk (R) Invetor (R) part file's (IPT) graphics data.
The importer can read files from Autodesk (R) Invetor (R) Inventro V2010 on. Older versions will fail!
'''

import traceback, importerSegNode
from importerSegment        import checkReadAll
from importerEeScene        import EeSceneReader
from importerTransformation import Transformation
from importerUtils          import *
from math import fabs

__author__     = 'Jens M. Plonka'
__copyright__  = 'Copyright 2018, Germany'
__url__        = "https://www.github.com/jmplonka/InventorLoader"

class GraphicsReader(EeSceneReader):

	def __init__(self, segment):
		super(GraphicsReader, self).__init__(segment)
		segment.meshes = {}

	def ReadIndexDC(self, node, i):
		i = node.ReadUInt32(i, 'indexDC')
		self.segment.indexNodes[node.get('indexDC')] = node
		return i

	def Read_HeaderParent(self, node, typeName = None):
		if (typeName is not None): node.typeName = typeName
		i = self.skipBlockSize(0, 8)
		i = node.ReadParentRef(i)
		i = self.skipBlockSize(i)
		return i

	def Read_Float32Arr(self, offset, node, name):
		cnt0, i = getUInt32(node.data, offset)
		i = node.ReadUInt32A(i, 2, 'Float32Arr_' + name)

		lst = []
		l2  = []
		for j in range(cnt0):
			a1, i = getFloat32_2D(node.data, i)
			lst.append(a1)
			vec = FloatArr2Str(a1)
			l2.append('(%s)' %(vec))

		if (len(l2) > 0):
			node.content += ' {%s}' %(','.join(l2))
		node.set(name, lst)
		return i

	def Read_Float64Arr(self, offset, node, size, name):
		cnt0, i = getUInt32(node.data, offset)
		i = node.ReadUInt32A(i, 2, 'Float64Arr_' + name)

		lst = []
		l2 = []
		for j in range(cnt0):
			a1, i = getFloat64A(node.data, i, size)
			lst.append(a1)
			vec = FloatArr2Str(a1)
			l2.append('(%s)' %(vec))

		if (len(l2) > 0):
			node.content += ' {%s}' %(','.join(l2))
		node.set(name, lst)
		return i

	def ReadDimensioning(self, node): # Dimensioning
		i = self.Read_32RRR2(node, 'Dimensioning')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadUInt32(i, 'key')
		i = node.ReadUInt8(i, 'u8_1')
		return i

	def Read_022AC1B1(self, node):
		i = node.ReadUInt8(0, 'u8')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		return i

	def Read_022AC1B5(self, node): # PartDrawAttr
		i = self.ReadHeaderSU32S(node, 'PartDrawAttr')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')

		if (getFileVersion() >= 2015):
			i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		else:
			i = node.ReadUInt16A(i, 2, 'a1')

		i = node.ReadUInt16A(i, 3, 'a2')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 2, 'a0')
		return i

	def Read_0244393C(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'keyRef')
		return i

	def Read_0270FFC7(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_2')
		return i

	def Read_03E3D90B(self, node):
		i = self.Read_HeaderParent(node, 'SurfaceCylinder')
		i = node.ReadList2(i, importerSegNode._TYP_SINT32_A_, 'lst0', 2)
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadFloat64_3D(i, 'vec_1')
		i = node.ReadFloat64_3D(i, 'vec_2')
		return i

	def Read_04F234D9(self, node): return 0

	def Read_05CE4AC7(self, node): return node.Read_Header0()

	def Read_097A6824(self, node): return 0

	def Read_0B2C8AE9(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadUInt16A(i, 4, 'a0')
		return i

	def Read_0BBBEBC8(self, node): return 0

	def Read_0BC8EA6D(self, node):
		i = self.Read_HeaderParent(node, 'KeyRef')
		i = node.ReadUInt32(i, 'key')
		return i

	def Read_0DE8E459(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadFloat64_3D(i, 'a3')
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_12A31E33(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 5, 'a0')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt16A(i, 8, 'a1')
		i = self.skipBlockSize(i, 8)
		return i

	def Read_14533D82(self, node): # WrkPlane
		i = self.ReadHeaderU32RefU8List3(node, 'WrkPlane')
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt32(i, 'index')
		i = self.ReadIndexDC(node, i)
		i = node.ReadFloat64A(i, 6, 'a1')
		i = self.ReadTransformation(node, i)
		i = node.ReadUInt8A(i, 3, 'a3')
		return i

	def Read_184FDA9C(self, node): return 0

	def Read_189725D1(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i  = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16(i, 'u16_0')
		return i

	def Read_2116098E(self, node): return 0

	def Read_23974603(self, node): return 0

	def Read_23ADA14E(self, node): return 0

	def Read_27F6DF59(self, node): return node.Read_Header0()

	def Read_2C7020F6(self, node): # WrkAxis
		i = self.ReadHeaderU32RefU8List3(node, 'WrkAxis')
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt32(i, 'index')
		i = self.ReadIndexDC(node, i)
		i = self.ReadTransformation(node, i)
		i = node.ReadUInt8A(i, 3, 'a3')
		return i

	def Read_2C7020F8(self, node): # WrkPoint
		i = self.ReadHeaderU32RefU8List3(node, 'WrkPoint')
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt32(i, 'index')
		i = self.ReadIndexDC(node, i)
		i = self.ReadTransformation(node, i)
		i = node.ReadUInt8A(i, 2, 'a3')
		return i

	def Read_35E93051(self, node):
		i = node.ReadUInt32(0, 'u32_0')
		i = node.ReadUInt8(0, 'u8_0')
		i = node.ReadUInt32(0, 'u32_1')
		return i

	def Read_37DB9D1E(self, node):
		node.typeName = 'SurfacePlane'
		i = self.skipBlockSize(0, 8)
		i = node.ReadParentRef(i)
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_SINT32_A_, 'lst0', 2)
		return i

	def Read_3A5FA872(self, node): return 0

	def Read_3D953EB2(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32A(i, 2, 'a1')
		return i

	def Read_3DA2C291(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt8A(i, 4, 'a2')
		return i

	def Read_3EA856AC(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32A(i, 2, 'a0')
		return i

	def Read_41305114(self, node):
		i = self.Read_32RRR2(node)
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadFloat32(i, 'f32_0')
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadFloat32A(i, 5, 'a0')
		i = node.ReadUInt16(i, 'u16_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_424221E2(self, node): return 0

	def Read_438452F0(self, node):
		i = node.ReadUInt16A(0, 4, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.skipBlockSize(i)
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 5, 'a0')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt16A(i, 8, 'a1')
		i = self.skipBlockSize(i, 8)
		return i

	def Read_4AD05620(self, node): # KeyRef
		i = self.Read_HeaderParent(node, 'KeyRef')
		i = node.ReadUInt32(i, 'key')
		return i

	def Read_4B26ED59(self, node): # Mesh
		i = self.ReadHeaderU32RefU8List3(node, 'Mesh', 'parts')
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = self.ReadIndexDC(node, i)
		if (getFileVersion() > 2017): i += 4 # FF,FF,FF,FF
		return i

	def Read_4B57DC55(self, node): # 2dCircle
		i = self.Read_32RRR2(node, '2dCircle')
		i = node.ReadFloat64_3D(i, 'm')
		i = node.ReadFloat64(i, 'f64_0')
		i = node.ReadFloat64(i, 'r')
		# start angle
		i = node.ReadAngle(i, 'alpha')
		# stop angle
		i = node.ReadAngle(i, 'beta')
		return i

	def Read_4B57DC56(self, node): # Ellipse3D
		i = self.Read_32RRR2(node, 'Ellipse3D')
		i = node.ReadFloat64_2D(i, 'c')
		i = node.ReadFloat64(i, 'b')      # length for point B
		i = node.ReadFloat64(i, 'a')      # length for point A
		i = node.ReadFloat64_2D(i, 'dB') # direction vector-2D for point B
		i = node.ReadFloat64_2D(i, 'dA') # direction vector-2D for point A
		# start angle
		i = node.ReadAngle(i, 'alpha')
		# stop angle
		i = node.ReadAngle(i, 'beta')
		return i

	def Read_4E951290(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		return i

	def Read_4E951291(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadLen32Text16(i)
		return i

	def Read_50E809CD(self, node): # Points
		i = self.Read_32RRR2(node, 'Points')
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'points', 3)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_UINT16_A_, 'lst1', 2)
		return i

	def Read_5194E9A2(self, node):
		i = self.Read_32RRR2(node)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadFloat64_3D(i, 'a0')
		i = node.ReadFloat64_3D(i, 'a1')
		return i

	def Read_56235A51(self, node): return 0

	def Read_591E9565(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32A(i, 2, 'a0')
		return i

	def Read_5D916CE9(self, node):
		i = self.Read_HeaderParent(node, 'KeyRef')
		i = node.ReadUInt32(i, 'key')
		return i

	def Read_5EDE1890(self, node): # Mesh
		i = self.ReadHeaderU32RefU8List3(node, 'Mesh', 'parts')
		i = node.ReadLen32Text16(i, 'meshId')
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadChildRef(i, 'ref_1')
		self.segment.meshes[node.get('meshId')] = node
		return i

	def Read_60FD1845(self, node): # Sketch2D
		i = self.ReadHeaderU32RefU8List3(node, 'Sketch2D')
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'key')
		i = self.ReadTransformation(node, i)
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst2')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst3')
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_6266D8CD(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt32A(i, 3, 'a0')
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst0', 3)
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadFloat32_3D(i, 'a2')
		i = self.skipBlockSize(i)
		i = node.ReadFloat32_3D(i, 'a3')
		i = self.skipBlockSize(i)
		return i

	def Read_651117CE(self, node): # MeshTriangleNormals
		i = node.Read_Header0('MeshTriangleNormals')
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'normals', 3)
		i = node.ReadUInt32(i, 'u32_1')
		if (getFileVersion() > 2013):
			i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		else:
			node.set('lst1', [])
		return i

	def Read_698CF98E(self, node): return 0

	def Read_6A05AA75(self, node): return node.Read_Header0()

	def Read_6A6931DC(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.ReadTypedFloatsList(node, i, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst1')
		i = node.ReadFloat64_3D(i, 'p1')
		i = node.ReadFloat64_3D(i, 'p2')
		return i

	def Read_6C8A5C53(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadFloat64A(i, 6, 'a4')
		i = node.ReadUInt8A(i, 4, 'a5')
		return i

	def Read_733CA999(self, node): return node.Read_Header0()

	def Read_76986821(self, node): return 0

	def Read_7DFC2448(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadCrossRef(i, 'ref_0')
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadUInt32(i, 'key')
		return i

	def Read_8DA49A23(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt16A(i, 4, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 5, 'a1')
		i = self.skipBlockSize(i, 8)
		i = node.ReadUInt16A(i, 4, 'a2')
		return i

	def Read_9215A162(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_913D5CD2(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_9360CF4D(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadFloat64(i, 'f64_0')
		if (getFileVersion() > 2013):
			i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		else:
			node.set('lst1', [])
		return i

	def Read_9516E3A1(self, node):
		return self.ReadDimensioning(node)

	def Read_9823F7FF(self, node): return node.Read_Header0()

	def Read_995AA46F(self, node): return node.Read_Header0()

	def Read_9A5F40BC(self, node): return node.Read_Header0()

	def Read_9A676A50(self, node): # Body
		i = node.Read_Header0('Body')
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadChildRef(i, 'ref0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadParentRef(i)
		i = self.ReadIndexDC(node, i) # SurfaceBody's index in DC-Segment
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt32(i, 'index')
		i = node.ReadChildRef(i, 'ref1')
		i = node.ReadUInt32A(i , 3, 'a0')
		i = node.ReadUInt16(i, 'u16_0')
		i = node.ReadChildRef(i, 'ref2')
		i = node.ReadChildRef(i, 'ref3')
		i = node.ReadChildRef(i, 'ref4')
		i = node.ReadChildRef(i, 'ref5')
		i = node.ReadChildRef(i, 'ref6')
		i = node.ReadList2(i, importerSegNode._TYP_2D_F64_U32_4D_U8_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadFloat64_2D(i, 'a2')
		i = self.skipBlockSize(i, 8)
		i = node.ReadList7(i, importerSegNode._TYP_MAP_U32_U32_, 'lst1')

#		i = node.ReadUInt16A(i, 4, 'a3')
#		a4, dummy = getUInt16A(node.data, i, 2)
#		if (a4[0] == 0x02 and a4[1] == 0x3000):
#			i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst2')
#			i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst3')
#			i = node.ReadUInt16A(i, 2, 'a4')
#		else:
#			node.set('lst0', [])
#			node.set('lst1', [])
#			i = dummy
#
#		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_9E2FB889(self, node): return 0

	def Read_9E8CE961(self, node): return 0

	def Read_9EA0717F(self, node): return node.Read_Header0()

	def Read_A3EBE198(self, node): return 0

	def Read_A6DD2FCC(self, node): return 0

	def Read_A79EACC7(self, node): # Line3D
		i = self.Read_32RRR2(node, 'Line3D')
		i = node.ReadFloat64(i, 'x')
		i = node.ReadFloat64(i, 'y')
		i = node.ReadFloat64(i, 'z')
		i = node.ReadFloat64(i, 'dirX')
		i = node.ReadFloat64(i, 'dirY')
		i = node.ReadFloat64(i, 'dirZ')
		return i

	def Read_A79EACCC(self, node): # Circle3D
		i = self.Read_32RRR2(node, 'Circle3D')
		i = node.ReadFloat64(i, 'x')
		i = node.ReadFloat64(i, 'y')
		i = node.ReadFloat64(i, 'z')
		i = node.ReadFloat64_3D(i, 'normal')
		i = node.ReadFloat64_3D(i, 'm')
		i = node.ReadFloat64(i, 'r')
		i = node.ReadFloat64(i, 'startAngle')
		i = node.ReadFloat64(i, 'sweepAngle')
		node.set('points', [])
		return i

	def Read_A79EACCD(self, node): return node.Read_Header0()

	def Read_A79EACD1(self, node): return node.Read_Header0()

#	def Read_A79EACD2(self, node):
#		i = 0
#		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst0', 3)
#		i = node.ReadList2(i, importerSegNode._TYP_UINT16_A_,  'lst1', 2)
#		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst2', 3)
#		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'lst3', 2)
#		i = node.ReadUInt16A(i, 2, 'a0')
#		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst4')
#		i = node.ReadFloat32_2D(i, 'a1')
# 		return i

	def Read_A79EACD3(self, node): # Point3D
		i = self.Read_32RRR2(node, 'Point3D')
		i = node.ReadFloat64(i, 'x')
		i = node.ReadFloat64(i, 'y')
		i = node.ReadFloat64(i, 'z')
		i = node.ReadFloat32(i, 'f32_0')
		i = node.ReadSInt32(i, 's32_0')
		i = node.ReadUInt16(i, 'u16_0')
		return i

	def Read_A79EACD5(self, node): # 2dText
		i = self.Read_32RRR2(node, '2dText')
		i = node.ReadLen32Text16(i )
		i = node.ReadFloat64_3D(i , 'vec')
		i = node.ReadFloat64_3D(i , 'a0')
		i = node.ReadUInt16A(i, 3, 'a1')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_A94779E0(self, node):
		'''
		SingleFeatureOutline
		'''
		node.typeName = 'SingleFeatureOutline'
		i = self.skipBlockSize(0)
		i = node.ReadParentRef(i)
		i = node.ReadUInt16A(i, 2, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'key')
		i = node.ReadFloat64A(i, 3, 'a1')
		i = node.ReadFloat64A(i, 3, 'a2')
		i = self.ReadTypedFloatsList(node, i, 'a3')
		i = node.ReadList2(i, importerSegNode._TYP_LIST_FLOAT64_A_, 'lst0', 3)
		return i

	def Read_A94779E2(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadParentRef(i)
		i = node.ReadUInt16A(i, 2, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadUInt16A(i, 4, 'a2')
		i = node.ReadFloat64A(i, 3, 'a3')
		i = node.ReadFloat64A(i, 3, 'a4')
		return i

	def Read_A94779E3(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadParentRef(i)
		i = node.ReadUInt16A(i, 2, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadUInt16A(i, 2, 'a1')
		i = node.ReadUInt32(i, 'key')
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadUInt32(i, 'u32_1')
		if (node.get('u32_1') == 1):
			i = node.ReadFloat64A(i, 6, 'a2')
		else:
			node.content += ' a2=()'
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadFloat64A(i, 6, 'a3')
		i = node.ReadUInt8A(i, 2, 'a4')
		i = self.ReadTypedFloatsList(node, i, 'a5')
		return i

	def Read_A94779E4(self, node):
		i = self.skipBlockSize(0)
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadUInt32A(i, 2, 'a0')
		cnt, i = getUInt32(node.data, i)
		i = self.ReadFloat64A(node, i, cnt, 'a1', 12)
		cnt, i = getUInt32(node.data, i)
		i = self.ReadFloat64A(node, i, cnt, 'a2', 6)
		i = self.ReadTypedFloatsList(node, i, 'a3')
		i = node.ReadFloat64A(i, 6, 'a4')
		i = node.ReadUInt8A(i, 2, 'a5')
		i = self.ReadTypedFloatsList(node, i, 'a6')
		i = node.ReadList2(i, importerSegNode._TYP_LIST_FLOAT64_A_, 'lst2', 3)
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadFloat64A(i, 9, 'a7')
		return i

	def Read_A98235C4(self, node):
		i = self.ReadHeaderU32RefU8List3(node, 'MeshPart')
		i = node.ReadChildRef(i, 'ref3dObject')
		i = self.skipBlockSize(i)
		i = self.ReadTransformation(node, i)
		i = node.ReadUInt32(i, 'u32_1')

		if (getFileVersion() < 2012):
			i = node.ReadUInt16A(i, 5, 'a2')
		else:
			i = node.ReadLen32Text16(i, 'txt0')
			i = node.ReadLen32Text16(i, 'txt1')

		if (node.get('u32_1') == 1):
			i = node.ReadUInt32A(i, 3, 'a3')
			i = node.ReadFloat64(i, 'f64_0')
			i = node.ReadUInt8(i, 'u8_0')
		else:
			node.set('a3', [0, 0, 0])
			node.set('f64_0', 0.0)
			node.content += u" a3=[0000,0000,0000] f64_0=0.0"
#			i = node.ReadLen32Text16(i, 'txt2')
		return i

	def Read_AC007F7A(self, node): return node.Read_Header0()

	def Read_AFD5CEEB(self, node): return 0

	def Read_B01025BF(self, node):
		return self.ReadDimensioning(node)

	def Read_B069BC6A(self, node):
		i = self.Read_32RRR2(node)
		i = node.ReadUInt16A(i, 8, 'a0')
		return i

	def Read_B1057BE1(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 13, 'a0')
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		return i

	def Read_B1057BE2(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 13, 'a0')
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		return i

	def Read_B1057BE3(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 13, 'a0')
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		return i

	def Read_B247B180(self, node): return 0

	def Read_B3895BC2(self, node):
		i = node.ReadUInt32A(0, 2, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_ColorAttr(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 5, 'a1')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt16A(i, 8, 'a2')
		i = self.skipBlockSize(i, 8)
		return i

	def Read_B9274CE3(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32(i, 'key')
		return i

	def Read_BCC1E889(self, node):
		return self.ReadDimensioning(node)

	def Read_BD5BB62B(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32(i, 'key')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_C0014C89(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt16A(i, 4, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadFloat64_2D(i, 'a1')
		i = node.ReadUInt8A(i, 4, 'a2')
		i = self.ReadTransformation(node, i)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 7, 'a5')
		return i

	def Read_C18CE1AF(self, node): return node.Read_Header0()

	def Read_C2A055C9(self, node): # MeshFolder
		i = self.ReadHeaderU32RefU8List3(node, 'MeshFolder', 'meshes')
		i = node.ReadUInt32(i, 'index')
		i = self.ReadIndexDC(node, i)
		if (getFileVersion() > 2017):
			i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		else:
			node.content += u" lst0={}"
		return i

	def Read_C2F1F8ED(self, node):
		return self.ReadDimensioning(node)

	def Read_C3608DE7(self, node): return node.Read_Header0()

	def Read_C46B45C9(self, node):
		return self.ReadDimensioning(node)

	def Read_C84E693F(self, node): return node.Read_Header0()

	def Read_C9DA5109(self, node):
		i = self.ReadHeaderSU32S(node)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_GUESS_, 'lst0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_CA7163A3(self, node):
		i = self.ReadHeaderU32RefU8List3(node)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		i = self.skipBlockSize(i)
		i = node.ReadColorRGBA(i, 'c0')
		i = node.ReadColorRGBA(i, 'c1')
		i = node.ReadColorRGBA(i, 'c2')
		i = node.ReadColorRGBA(i, 'c3')
		i = node.ReadFloat32(i, 'f32_0')
		i = self.skipBlockSize(i)
		return i

	def Read_D1071D57(self, node):
		i = self.Read_32RRR2(node)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		a3, i = getUInt16A(node.data, i, 2)
#		i = self.ReadTransformation(node, i)
		return i

	def Read_D28CA9B4(self, node): return 0

	def Read_D3A55701(self, node): # 2dSpline
		i = self.Read_32RRR2(node, '2dSpline')
		i = node.ReadUInt32A(i, 3, 'a0')
		i = node.ReadUInt8A(i, 8, 'a1')
		i = self.Read_Float32Arr(i, node, 'lst0')
		i = self.Read_Float32Arr(i, node, 'lst1')
		i = self.Read_Float64Arr(i, node, 2, 'lst2')
		i = node.ReadUInt8A(i, 8, 'a2')
		i = node.ReadUInt32A(i, 2, 'a3')
		i = node.ReadFloat64_2D(i, 'a4')
		i = self.Read_Float64Arr(i, node, 2, 'lst3')
		return i

	def Read_D3A55702(self, node): # Spline3D_Curve
		i = self.Read_32RRR2(node, 'Spline3D_Curve')
		i = node.ReadUInt32A(i, 3, 'a0')
		i = node.ReadUInt8A(i, 8, 'a1')
		i = self.Read_Float32Arr(i, node, 'lst0')
		i = self.Read_Float32Arr(i, node, 'lst1')
		i = self.Read_Float64Arr(i, node, 3, 'lst2')
		i = node.ReadUInt8A(i, 8, 'a2')
		i = node.ReadUInt32A(i, 2, 'a3')
		i = node.ReadFloat64_2D(i, 'a4')
		return i

	def Read_D4824069(self, node): # Mesh folder
		i = self.ReadHeaderU32RefU8List3(node, 'Mesh2', 'meshes')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadUInt32(i, 'index')
		i = self.ReadIndexDC(node, i)
		return i

	def Read_D79AD3F3(self, node):
		i = self.Read_A79EACD2(node)
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst5')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst6')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst7')
		return i

	def Read_DA58AA0E(self, node): # Sketch3D
		i = self.ReadHeaderU32RefU8List3(node, 'Sketch3D')
		i = node.ReadChildRef(i, 'ref_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt8(i, 'u8_1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'key')
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		i = node.ReadUInt8(i, 'u8_2')
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst2')
		i = node.ReadUInt8(i, 'u8_3')
		return i

	def Read_DBE41D91(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt16A(i, 4, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		i = node.ReadFloat64_3D(i, 'a1')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32A(i, 14, 'a2')
		return i

	def Read_DEF9AD02(self, node): # MeshTrianglePoints
		i = node.Read_Header0('MeshTrianglePoints')
		i = node.ReadList2(i, importerSegNode._TYP_FLOAT32_A_, 'points', 3)
		i = node.ReadUInt32(i, 'u32_1')
		if (getFileVersion() > 2013):
			i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		else:
			node.set('lst1', [])
		return i

	def Read_DEF9AD03(self, node): # MeshTriangleIndices
		i = node.Read_Header0('MeshTriangleIndices')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'indices')
		i = node.ReadUInt32(i, 'u32_1')
		if (getFileVersion() > 2013):
			i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst1')
		else:
			node.set('lst1', [])
		return i

	def Read_E1EB685C(self, node): # MeshFacets
		i = self.Read_32RRR2(node, 'MeshFacets')
		i = node.ReadChildRef(i, 'points')
		i = node.ReadChildRef(i, 'pointIndices')
		i = node.ReadChildRef(i, 'normals')
		i = node.ReadChildRef(i, 'normalIndices')
		i = node.ReadUInt32A(i, 5, 'a0')
		i = node.ReadList2(i, importerSegNode._TYP_GUESS_, 'lst0')
		i = node.ReadUInt32A(i, 2, 'a1')
		return i

	def Read_EF1E3BE5(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_FONT_, 'lst0')
		return i

	def Read_F6ADCC68(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_F6ADCC69(self, node):
		i = self.Read_HeaderParent(node)
		i = node.ReadUInt32(i, 'index')
		return i

	def Read_F96556CB(self, node): # MeshPart
		i = self.ReadHeaderU32RefU8List3(node, 'MeshPart')
		i = node.ReadChildRef(i, 'ref3dObject')
		i = node.ReadParentRef(i)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadUInt8A(i, 2, 'a1')
		i = self.ReadIndexDC(node, i)
		if (getFileVersion() > 2017):
			i = node.ReadList2(i, importerSegNode._TYP_SINT32_, 'lst1')
		else:
			node.content += u" lst1=[]"
		return i

	def Read_F9C49549(self, node): return node.Read_Header0()

	def Read_FB96D24A(self, node):
		i = node.Read_Header0()
		i = node.ReadUInt16A(i, 4, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadFloat64_3D(i, 'f64_0')
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_FE59A112(self, node): return node.Read_Header0()

	def Read_FF084971(self, node):
		return self.ReadDimensioning(node)

	def Read_FFB5643C(self, node):
		return self.ReadDimensioning(node)
