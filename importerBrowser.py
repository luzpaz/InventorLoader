# -*- coding: utf-8 -*-

'''
importerBrowser.py:
Simple approach to read/analyse Autodesk (R) Invetor (R) part file's (IPT) browser view data.
The importer can read files from Autodesk (R) Invetor (R) Inventro V2010 on. Older versions will fail!
'''

from importerSegment import SegmentReader, checkReadAll
from importerUtils   import *
import importerSegNode

__author__     = "Jens M. Plonka"
__copyright__  = 'Copyright 2018, Germany'
__url__        = "https://www.github.com/jmplonka/InventorLoader"

class BrowserReader(SegmentReader):

	def __init__(self, segment):
		super(BrowserReader, self).__init__(segment)
		self.__Str53_u16_0 = 0

	def Read_Str53(self, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = node.ReadLen32Text16(0)
		i = node.ReadUInt32(i, 'flags')
		b, i = getBoolean(node.data, i)
		if (b):
			i = node.ReadUInt16(i, 'u16_0')
			self.__Str53_u16_0 = node.get('u16_0')
		else:
			self.__Str53_u16_0 += 1
			node.set('u16_0', self.__Str53_u16_0)
			node.content += u' u16_0=%03X' % self.__Str53_u16_0
		i = node.ReadUInt16A(i, 3, 'a1')

		i = self.skipBlockSize(i)
		return i

	def Read_Str01(self, offset, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = node.ReadLen32Text16(offset)
		i = node.ReadLen32Text16(i, 'txt_1')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_Str23(self, offset, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = node.ReadLen32Text16(offset, 'txt_2')
		i = node.ReadLen32Text16(i, 'txt_3')
		i = node.ReadSInt32A(i, 3, 'a1')
		i = self.skipBlockSize(i)
		return i

	def Read_664(self, offset, node):
		i = node.ReadUInt32(offset, 'index')
		i = node.ReadUInt16A(i, 4, 'a2')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt16A(i, 6, 'a3')
		i = node.ReadUInt8(i, 'u8_2')
		i = node.ReadUInt32(i, 'grIdx')
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadUInt8(i, 'u8_3')
		i = self.skipBlockSize(i)
		return i

	def ReadHeader0_664(self, node, typeName = None):
		i = node.Read_Header0(typeName)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = self.Read_664(i, node)
		return i

	def ReadHeaderHospitalItem(self, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = node.ReadUInt32(0, 'u32_0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'key') # the list index
		i = self.skipBlockSize(i)
		return i

	def Read_09CB971A(self, node):
		i = node.ReadUInt32A(0, 2, 'a0')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst1')
		i = node.ReadSInt32A(i, 2, 'a1')
		return i

	def Read_189B3560(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadLen32Text16(i)
		i = node.ReadUInt32(i, 'grIdx')
		return i

	def Read_19910142(self, node): # 3rdParty
		i = self.ReadHeader0_664(node, '3rdParty')
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		return i

	def Read_1B16984A(self, node): # Hospital
		node.typeName = 'Hospital'
		i = node.ReadUInt16A(0, 3, 'a0')
		i = self.skipBlockSize(i, 8)
		i = node.ReadList6(i, importerSegNode._TYP_MAP_KEY_REF_, 'lst0')
		i = node.ReadUInt8(i, 'u8_0')
		return i

	def Read_037BF59B(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst1', 2)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadUInt32(i, 'u32_3')
		return i

	def Read_09CB9718(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		i = self.skipBlockSize(i)
		return i

	def Read_44DBCB35(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		i = self.skipBlockSize(i)
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_3')
		return i

	def Read_52879851(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		i = self.skipBlockSize(i)
		return i

	def Read_58B90125(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst1', 2)
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_AC1898AD(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		return i

	def Read_9B451345(self, node): # Hospital item
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadUInt32(i, 'u32_3')
		return i

	def Read_CF604E8B(self, node):
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_A_, 'lst1', 2)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadUInt8(i, 'u8_2')
		return i

	def Read_E7E4F967(self, node):
		i = self.ReadHeaderHospitalItem(node)
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadUInt32(i, 'u32_3')
		i = node.ReadUInt16(i, 'u16_2')
		return i

	def Read_44664C6F(self, node):
		i = self.ReadHeader0_664(node)
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		return i

	def Read_09CB9719(self, node):
		i = node.ReadUInt32A(0, 2, 'a0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst1')
		i = node.ReadSInt32A(i, 2, 'a1')
		return i

	def Read_75839EBD(self, node):
		i = node.ReadUInt32A(0, 2, 'a0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_UINT32_, 'lst1')
		i = node.ReadSInt32A(i, 2, 'a1')
		return i

	def Read_716B5CD1(self, node): # ATEntry
		i = self.ReadHeader0_664(node, 'AnalysisToolEntry')
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 4, 'a0')
		return i

	def Read_761C4FA0(self, node):
		i = self.Read_Str53(node)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadParentRef(i)
		i = node.ReadUInt16A(i, 4, '664.a0')
		i = node.ReadUInt8(i, '664.u8_0')
		i = node.ReadUInt16A(i, 6, '664.a1')
		i = node.ReadUInt8(i, '664.u8_1')
		i = node.ReadUInt32A(i, 2, '664.a2')
		i = node.ReadUInt8(i, '664.u8_2')
		i = self.skipBlockSize(i)
		i = self.skipBlockSize(i)
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_7DFCC817(self, node): # ConstructionFolderEntry
		i = self.ReadHeader0_664(node, 'ConstructionFolderEntry')
		i = self.Read_Str01(i, node)
		i = node.ReadSInt32(i, 's32_0')
		i = self.skipBlockSize(i)
		return i

	######
	# Folder Entries
	def Read_7DFCC818(self, node):
		i = self.ReadHeader0_664(node, 'FolderEntries')
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadSInt32(i, 's32_0')
		i = node.ReadLen32Text16(i, 'str0')
		i = node.ReadUInt32A(i, 2, 'a0')
		return i

	def ReadHeaderFolderEntry(self, node, typeName = None):
		i = self.ReadHeader0_664(node)
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadSInt32(i, 's32_0')
		i = self.Read_Str23(i, node)

	def Read_0E7F99A4(self, node):
		i = self.ReadHeaderFolderEntry(node, 'SurfaceEntry')
		return i

	def Read_0F590179(self, node):
		i = self.ReadHeaderFolderEntry(node, 'SolidEntry')
		return i

	def Read_67361CCF(self, node):
		i = self.ReadHeaderFolderEntry(node, 'DiagEntry')
		return i

	def Read_69A4ED42(self, node):
		i = self.ReadHeaderFolderEntry(node, 'WireEntry')
		return i

	def Read_89B87C6F(self, node): # DiagProfileInvalidLoop
		node.typeName = 'DiagProfileInvalidLoop'
		i = self.skipBlockSize(0)
		i = node.ReadUInt32A(i, 2, 'a0')
		i = self.skipBlockSize(i)
		return i

	#######
	# Part folder interfaces
	def Read_9E77CCC1(self, node):
		i = self.ReadHeader0_664(node, 'PartInterfaceFolder')
		i = node.ReadUInt16A(i, 2, 'a0')
		i = node.ReadLen32Text16(i)
		i = node.ReadUInt8(i, 'u8_0')
		i = self.skipBlockSize(i)
		return i

	def ReadHeaderPartInterface(self, node, typeName = None):
		i = self.ReadHeader0_664(node, typeName)
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 4, 'a4')
		i = self.skipBlockSize(i)
		return i

	def Read_9E77CCC3(self, node): # Part mate interface
		i = self.ReadHeaderPartInterface(node,'PartInterfaceMate')
		return i

	def Read_9E77CCC4(self, node): # Part flush interface
		i = self.ReadHeaderPartInterface(node, 'PartInterfaceFlush')
		return i

	def Read_9E77CCC5(self, node): # Part angle interface
		i = self.ReadHeaderPartInterface(node, 'PartInterfaceAngle')
		return i

	def Read_9E77CCC6(self, node): # Parttangent interface
		i = self.ReadHeaderPartInterface(node, 'PartInterfaceTangent')
		return i

	def Read_9E77CCC7(self, node): # Part insert interface
		i = self.ReadHeaderPartInterface(node, 'PartInterfaceInsert')
		return i

	def Read_E7EE0A91(self, node): # Part composite interface
		i = self.ReadHeaderPartInterface(node, 'PartInterfaceComposite')
		return i

	def Read_B251BFC0(self, node): # EntryManager
		i = node.Read_Header0('EntryManager')
		i = node.ReadList7(i, importerSegNode._TYP_MAP_KEY_REF_, 'entries')
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_B75AE9EF(self, node):
		i = node.ReadLen32Text16(0)
		i = node.ReadUInt8(i, 'u8_0')
		if (node.get('u8_0') > 0):
			i = node.ReadUInt32(i, 'u32_0')
#			i = node.ReadList1(i, importerSegNode._TYP_UINT8_, 'blob')
		else:
			i = node.ReadUInt16(i, 'u16_0')
			i = node.ReadLen32Text16(i, 'str0')
			i = node.ReadLen32Text16(i, 'str1')
			i = node.ReadSInt32A(i, 4, 'a1')
			i = node.ReadUInt8(i, 'u8_1')
			i = node.ReadUInt16(i, 'u16_1')
			i = node.ReadLen32Text16(i, 'str2')
			i = node.ReadLen32Text16(i, 'str3')
			i = node.ReadSInt32A(i, 2, 'a2')
		return i

	def Read_3683CE33(self, node): # RDxDiagSketchDimRefGeomFailed
		node.typeName = "DiagSketchDimRefGeomFailed"
		i = node.ReadParentRef(0)
		i = node.ReadUInt32A(i, 3, 'a0')
		return i

	def Read_CBBCFA51(self, node):
		i = node.ReadParentRef(0)
		i = node.ReadUInt32A(i, 3, 'a0')
		i = node.ReadUInt32(i, 'mask')
		return i

	def Read_D2B2DF09(self, node):
		# Only found in Bauteil001 and Bauteil002
		i = node.Read_Header0()
		i = node.ReadUInt16(i, 'u16_0')
		i = node.ReadList2(i,  importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_D81CDE47(self, node): # NBxEntry
		i = self.ReadHeader0_664(node, 'NBxEntry')
		i = node.ReadLen32Text16(i)
		i = node.ReadLen32Text16(i, 'str0')
		i = self.skipBlockSize(i)
		i = node.ReadUInt16A(i, 3, 'a4')
		i = node.ReadUInt8(i, 'u8_4')
		return i

	def Read_D9389A04(self, node):
		i = node.ReadUInt16A(0, 10, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i,  importerSegNode._TYP_NODE_X_REF_, 'lst0')
		i = node.ReadUInt32A(i, 3, 'a1')
		i = node.ReadBoolean(i, 'b0')
		i = node.ReadUInt32A(i, 3, 'a2')
		i = node.ReadBoolean(i, 'b1')
		i = node.ReadUInt32A(i, 2, 'a3')
		i = node.ReadBoolean(i, 'b2')
		i = self.skipBlockSize(i, 12)
		return i

	def Read_D95A2DF2(self, node): # TranslationReport
		i = self.ReadHeader0_664(node, 'TranslationReport')
		i = self.Read_Str01(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadSInt32(i, 's32_0')
		i = node.ReadLen32Text16(i, 'str2')
		i = node.ReadLen32Text16(i, 'str3')
		i = node.ReadChildRef(i, 'ref_0')
		return i

	def Read_DDC7ED24(self, node):
		i = node.Read_Header0()
		i = self.skipBlockSize(i)
		i = node.ReadUUID(i, 'uid_0')
		i = node.ReadLen32Text16(i)
		i = node.ReadUInt32(i, 'u32_0')
		return i

	def Read_DF9CA7B0(self, node):
		i = node.Read_Header0()
		i = node.ReadParentRef(i)
		i = node.ReadCrossRef(i, 'ref_0')
		i = node.ReadLen32Text16(i)
		i = node.ReadList4(i, importerSegNode._TYP_STRING8_, 'lst0')
		i = node.ReadUInt16(i, 'u16')
		i = node.ReadLen32Text16(i, 'val')
		return i

	def Read_E079A121(self, node):
		i = self.ReadHeaderEntry(node)
		if (getFileVersion() > 2016):
			i = node.ReadLen32Text16(i, 'txt0')
		return i

	def Read_F1EDED3E(self, node):
		i = self.ReadHeaderEntry(node)
		return i

	def Read_F757BC76(self, node):
		i = node.Read_Header0()
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadUInt32A(i, 2, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = self.ReadNodeRefs(node, i, 'lst1', importerSegNode.REF_CHILD)
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadChildRef(i, 'ref_1')
		i = node.ReadUInt32A(i, 2, 'a1')
		i = node.ReadUInt32(i, 'u32_0')
		i = node.ReadUInt8A(i, 5, 'a2')
		i = self.skipBlockSize(i)
		i = node.ReadLen32Text16(i)
		i = node.ReadLen32Text16(i, 'str1')
		i = node.ReadLen32Text16(i, 'str2')
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst1')
		i = node.ReadUInt8(i, 'u8_2')
		i = self.skipBlockSize(i)
		# 01 01 B7 00 00 00 00 00 00
		return i

	##################
	# Manager Entries

	def ReadHeaderEntry(self, node, typeName = None):
		i = self.Read_Str53(node, typeName)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'items')
		i = self.Read_664(i, node)
		i = self.skipBlockSize(i)
		node.Entry = True
		return i

	def Read_50C73580(self, node): # 3D-Object
		i = self.ReadHeaderEntry(node, '3dObject')
		i = node.ReadUInt8(i, 'u8_5')

		if (getFileVersion() > 2016):
			dummy, i = getUInt32A(node.data, i, 2)
		return i

	def Read_4D0B0CC5(self, node): # Text annotation
		i = self.ReadHeaderEntry(node, 'AnnotationText')
		i = node.ReadUInt32A(i, 3, 'a4')
		cnt, i = getUInt32(node.data, i)
		node.ReadUInt16A(i, cnt, 'a5')
		return i

	def Read_F8EEAD15(self, node): # Base
		i = self.ReadHeaderEntry(node, 'Base')
		return i

	def Read_DD1ADF96(self, node): # Body
		i = self.ReadHeaderEntry(node, 'Body')
		i = node.ReadUInt32(i, 'dcCreatorIdx')
		i = node.ReadUInt32A(i, 2, 'a5')
		return i

	def Read_8E50B102(self, node): # Block
		i = self.ReadHeaderEntry(node, 'Block')
		return i

	def Read_330C8EC7(self, node): # Blocks
		i = self.ReadHeaderEntry(node, 'Blocks')
		return i

	def Read_0C775998(self, node): # Annotations folder
		i = self.ReadHeaderEntry(node, 'FolderAnnotations')
		i = node.ReadUInt32(i, 'folderIdx')
		return i

	def Read_240BF169(self, node): # Bodies folder
		i = self.ReadHeaderEntry(node, 'FolderBodies')
		return i

	def Read_6CDD3AB0(self, node): # Browser folder
		i = self.ReadHeaderEntry(node, 'FolderBrowser')
		return i

	def Read_7FC32FE5(self, node): # UCS Folder
		i = self.ReadHeaderEntry(node, 'FolderUCS')
		return i

	def Read_BF03D5B6(self, node): # Contour Flange
		i = self.ReadHeaderEntry(node, 'ContourFlange')
		return i

	def Read_91D23C62(self, node): # Cropping
		i = self.ReadHeaderEntry(node, 'Cropping')
		return i

	def Read_82EBFBD9(self, node): # Direct Edit
		i = self.ReadHeaderEntry(node, 'DirectEdit')
		return i

	def Read_36F8D245(self, node): # Drawing
		i = self.ReadHeaderEntry(node, 'Drawing')
		return i

	def Read_8C5986A1(self, node): # Edges
		i = self.ReadHeaderEntry(node, 'Edges')
		i = node.ReadUInt16A(i, 2, 'a4')
		i = node.ReadUInt32(i, 'NtIdx')
		return i

	def Read_9C8323E5(self, node): # 2D Equation Curve
		i = self.ReadHeaderEntry(node, 'EquationCurve2D')
		return i

	def Read_D6AB5953(self, node): # 3d Equation Curve
		i = self.ReadHeaderEntry(node, 'EquationCurve3D')
		return i

	def Read_11D83D80(self, node): # EndOfPart
		i = self.ReadHeaderEntry(node, 'EndOfPart')
		return i

	def Read_9632B3FA(self, node): # Face
		i = self.ReadHeaderEntry(node, 'Face')
		i = self.skipBlockSize(i)
		return i

	def Read_F7676AB2(self, node): # Feature
		i = self.ReadHeaderEntry(node, 'Feature')
		i = node.ReadUUID(i, 'uid_0')
		i = node.ReadUInt32(i, 'u32_1')
		if (getFileVersion() > 2011):
			i = node.ReadLen32Text16(i, 'txt_0')
			i = node.ReadSInt32(i, 's32_0')
		else:
			node.content += u" txt_0='' s32_0=-1"
			node.set('txt_0', '')
			node.set('s32_0', -1)
		return i

	def Read_6531C640(self, node): # Flange
		i = self.ReadHeaderEntry(node, 'Flange')
		return i

	def Read_F99B4BFD(self, node): # Image
		i = self.ReadHeaderEntry(node, 'Image')
		return i

	def Read_1D8866A4(self, node): # 3D-Intersection
		i = self.ReadHeaderEntry(node, 'Intersection3D')
		return i

	def Read_E7A52E09(self, node): # Lofted Flange
		i = self.ReadHeaderEntry(node, 'LoftedFlange')
		return i

	def Read_8D0F39C2(self, node): # Matches
		i = self.ReadHeaderEntry(node, 'Matches')
		return i

	def Read_987C1C4E(self, node): # Matched Edge
		i = self.ReadHeaderEntry(node, 'MatchedEdge')
		return i

	def Read_363E8E7D(self, node): # Mesh Feature
		i = self.ReadHeaderEntry(node, 'MeshFeature')
		i = node.ReadUInt32A(i, 2, 'a4')
		return i

	def Read_87E10017(self, node): # Mesh folder
		i = self.ReadHeaderEntry(node, 'MeshFolder')
		i = node.ReadUInt32(i, 'u32_1')
		if (node.get('u32_1') == 1):
			i = node.ReadUInt32A(i, 5, 'a4')
		return i

	def Read_420BDF59(self, node): # Flat Pattern
		i = self.ReadHeaderEntry(node, 'PatternFlat')
		return i

	def Read_E14BDF12(self, node): # Pivot plate
		i = self.ReadHeaderEntry(node, 'PivotPlate')
		return i

	def Read_3E54E601(self, node): # Project to Surface
		i = self.ReadHeaderEntry(node, 'Project2Surface')
		i = node.ReadUInt32(i, 'u32_1')
		i = self.skipBlockSize(i)
		return i

	def Read_2B398DFB(self, node): # Project Cut Edge
		i = self.ReadHeaderEntry(node, 'ProjectCutEdge')
		return i

	def Read_A1DF3B79(self, node): # Projected Loop
		i = self.ReadHeaderEntry(node, 'ProjectedLoop')
		return i

	def Read_33DDFC82(self, node): # Reference
		i = self.ReadHeaderEntry(node, 'Reference')
		if (getFileVersion() > 2016):
			i = node.ReadLen32Text16(i, 'path')
		return i

	def Read_46DE5489(self, node): # Assembly reference
		i = self.ReadHeaderEntry(node, 'ReferenceAssembly')
		return i

	def Read_FCF044C3(self, node): # Part reference
		i = self.ReadHeaderEntry(node, 'ReferencePart')
		return i

	def Read_C0465062(self, node): # Solid reference
		i = self.ReadHeaderEntry(node, 'ReferenceSolid')
		i = node.ReadUUID(i, 'ui')
		return i

	def Read_EAFCF33F(self, node): # Surface reference
		i = self.ReadHeaderEntry(node, 'ReferenceSurface')
		i = node.ReadUUID(i, 'ui')
		return i

	def Read_DCB9673A(self, node): # Refold
		i = self.ReadHeaderEntry(node, 'Refold')
		return i

	def Read_F7676AB0(self, node): # 2D-Sketch
		i = self.ReadHeaderEntry(node, 'Sketch2D')
		return i

	def Read_4A156CBC(self, node): # 3D-Sketch
		i = self.ReadHeaderEntry(node, 'Sketch3D')
		return i

	def Read_2AC37C16(self, node): # Solid
		i = self.ReadHeaderEntry(node, 'Solid')
		return i

	def Read_BAF2D1C6(self, node): # spiral curve
		i = self.ReadHeaderEntry(node, 'SpiralCurve')
		return i

	def Read_84FA6B6C(self, node): # Table
		i = self.ReadHeaderEntry(node, 'Table')
		i = node.ReadUInt8A(i, 3, 'a0')
		i = node.ReadLen32Text16(i, 'str0')
		return i

	def Read_E84595D1(self, node): # Unfold
		i = self.ReadHeaderEntry(node, 'Unfold')
		return i

	def Read_74AD7D3C(self, node): # Wire
		i = self.ReadHeaderEntry(node, 'Wire')
		return i

	def Read_10B2DF6C(self, node): # ???.wire
		i = self.ReadHeaderEntry(node)
		return i

	def Read_E4B915DD(self, node): # iFeature:N
		i = self.ReadHeaderEntry(node)
		return i

	def Read_18BAA333(self, node): # ???
		i = self.ReadHeaderEntry(node)
		return i

	def Read_74EEF6B7(self, node): # ???
		i = self.ReadHeaderEntry(node)
		return i

	def Read_8BF242F4(self, node): # ???
		i = self.ReadHeaderEntry(node)
		i = node.ReadUInt16A(i, 2, 'a0')
		return i

	def Read_93C65F8A(self, node): # ???
		i = self.ReadHeaderEntry(node)
		return i

	def Read_9C599498(self, node): # ???
		i = self.ReadHeaderEntry(node)
		return i

	def Read_AF64BA30(self, node): # ???
		i = self.ReadHeaderEntry(node)
		cnt, i = getUInt32(node.data, i)
		lst = []
		for k in range(cnt):
			a, i = getUInt32A(node.data, i, 3)
			lst.append(a)
		node.content += u" lst4=[%s]" %(",".join(["(%04X,%04X,%04X)"%(a[0], a[1], a[2]) for a in lst]))
		node.set('lst4', lst)
		return i

	def Read_B4278FFF(self, node): # ???
		i = self.ReadHeaderEntry(node)
		return i

	def Read_E82BC461(self, node): # Slot Pattern
		vers = getFileVersion()
		i = node.ReadUInt32(0, 'u32_1')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst0')
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst1')
		if (vers > 2015):
			i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'lst2')
		else:
			i = node.ReadChildRef(i, 'ref_1')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadLen32Text16(i)
		i = node.ReadUInt8A(i, 5, 'a0')
		if (node.get('a0')[4] == 0):
			node.set('u16_0', 0)
		else:
			i = node.ReadUInt16(i, 'u16_0')
		i = node.ReadUInt16A(i, 3, 'a1')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_REF_, 'items')
		i = self.Read_664(i, node)
		i = self.skipBlockSize(i)
		i = node.ReadUUID(i, 'uid_0')
		i = node.ReadUInt32(i, 'u32_2')
		i = self.skipBlockSize(i)
		if (vers > 2010): i += 4 # skip 00 00 00 00
		if (vers > 2011): i += 4 # skip FF FF FF FF
		node.Entry = True
		return i

	def Read_F7676AB1(self, node): # ???
		i = node.ReadUInt32(0, 'flags')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadLen32Text16(i)
		i = node.ReadUInt8(i, 'u8_4')
		i = node.ReadUInt16A(i, 5, 'a0')
		i = self.skipBlockSize(i)
		i = node.ReadList2(i, importerSegNode._TYP_NODE_X_REF_, 'items')
		i = self.Read_664(i, node)
		i = self.skipBlockSize(i)
		node.Entry = True
		return i

	###########
	# Drawing

	def ReadHeaderDx(self, node, typeName = None):
		if (typeName is not None):
			node.typeName = typeName
		i = node.ReadUInt32(0, 'u32_0')
		i = node.ReadUInt16(i, 'u16_0')
		i = self.skipBlockSize(i)
		return i

	def ReadHeaderDxHierarchy(self, node, typeName = None):
		i = self.ReadHeaderDx(node,typeName)
		i = node.ReadList2(i, _TYP_NODE_REF_, 'items')
		i = node.ReadUInt32A(i, 2, 'a0')
		i = node.ReadUInt8(i, 'u8_0')
		i = node.ReadUInt32A(i, 4, 'a1')
		i = node.ReadUInt8(i, 'u8_1')
		i = node.ReadUInt32A(i, 2, 'a2')
		i = node.ReadUInt8(i, 'u8_2')
		i = self.skipBlockSize(i)
		i = node.ReadLen32Text16(i)
		i = node.ReadLen32Text16(i, 'group')
		i = node.ReadUInt8(i, 'u8_3')
		i = self.skipBlockSize(i)
		return i

	def Read_01E698C4(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_28F1F886(self, node):
		i = self.ReadHeaderDxHierarchy(node, 'Scene')
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_2F111558(self, node):
		i = self.ReadHeaderDxHierarchy(node, 'Tweak')
		if (getFileVersion() > 2017):
			x, i = getFloat64(node.data, i) # skip
		return i

	def Read_51F99C85(self, node): # DxBrowser
		i = self.ReadHeaderDxHierarchy(node, 'Presentation')
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_959A9EA0(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		i = node.ReadUInt32(i, 'u32_1')
		return i

	def Read_8CC74082(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_CACB745A(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_CACB745B(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_CACB745C(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_DB5B972C(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_FA0DFEE2(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_F4BF99A1(self, node):
		i = self.ReadHeaderDxHierarchy(node, 'TweakMember')
		i = node.ReadFloat64(i, 'x')
		return i

	def Read_246EF1E0(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_2AB35572(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA560(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA561(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA562(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA563(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA564(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA565(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA566(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA567(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA568(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6B6FA569(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		i = node.ReadBoolean(i, 'b0')
		i = node.ReadUInt32A(i, 3, 'a3')
		i = node.ReadList7(i, _TYP_MAP_KEY_REF_, 'entries')
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadBoolean(i, 'b1')
		i = node.ReadUInt32(i, 'u32_2')
		i = node.ReadBoolean(i, 'b2')
		if not node.get('b1'):
			i = node.ReadLen32Text16(i, 'category')
			i = node.ReadLen32Text16(i, 'id')
			i = node.ReadUInt16(i, 'u16_1')
		i = self.skipBlockSize(i)
		return i

	def Read_79EBBBEA(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_9200B040(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_B40C3AFC(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_C2D84C27(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		i = node.ReadUInt32(i, 'u32_1')
		i = node.ReadLen32Text16(i, 'part')
		return i

	def Read_214443B4(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_21DDD237(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_6263ECBE(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_8AE910D6(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_8FAF1C15(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_9200B041(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_98AB6133(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_B26F49F6(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_B26F49F7(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_B556DDFF(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_D8727CE1(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_E3656A31(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_F3FD738E(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_F5F3D48F(self, node):
		i = self.ReadHeaderDxHierarchy(node)
		return i

	def Read_16045A0A(self, node):
		i = self.ReadHeaderDx(node)
		# L L _ L S S
		return i

	def Read_69074B0B(self, node):
		i = self.ReadHeaderDx(node)
		# L L _ L S
		return i

	def Read_D29A65E5(self, node):
		i = self.ReadHeaderDx(node)
		# L L _ L _
		return i

	def Read_FC89C973(self, node):
		i = self.ReadHeaderDx(node)
		# L L _ L
		return i


	###########
	# Presentation
