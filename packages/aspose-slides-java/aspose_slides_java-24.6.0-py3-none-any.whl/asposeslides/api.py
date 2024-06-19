from __future__ import absolute_import

from enum import IntEnum
from array import array

from jpype import *
from jpype.types import *
from jpype import imports

from com.aspose.slides import StreamBuffer
@JImplementationFor("com.aspose.slides.StreamBuffer")
class _StreamBuffer(object):
    @JOverride(sticky=False)
    def write(self, chunk):
        if chunk == None:
            raise Exception("chunk is required")
        elif chunk.__class__.__name__ != 'bytes':
            raise TypeError("a bytes-like object is required")
        elif len(chunk) <= 0:
            raise ValueError("no content")
        self.writeStream(chunk, 0, len(chunk))

from com.aspose.slides import AdjustValue
from com.aspose.slides import AdjustValueCollection
from com.aspose.slides import AfterAnimationType
from com.aspose.slides import AlphaBiLevel
from com.aspose.slides import AlphaCeiling
from com.aspose.slides import AlphaFloor
from com.aspose.slides import AlphaInverse
from com.aspose.slides import AlphaModulate
from com.aspose.slides import AlphaModulateFixed
from com.aspose.slides import AlphaReplace
from com.aspose.slides import AnimateTextType
from com.aspose.slides import AnimationTimeLine
from com.aspose.slides import AsposeLicenseException
from com.aspose.slides import Audio
from com.aspose.slides import AudioCollection
@JImplementationFor("com.aspose.slides.AudioCollection")
class _AudioCollection(object):
	def addAudioFromBytes(self, *args):
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addAudio(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addAudio(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import AudioFrame
@JImplementationFor("com.aspose.slides.AudioFrame")
class _AudioFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import AudioPlayModePreset
from com.aspose.slides import AudioVolumeMode
from com.aspose.slides import AutoShape
@JImplementationFor("com.aspose.slides.AutoShape")
class _AutoShape(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import AutoShapeLock
from com.aspose.slides import AxesCompositionNotCombinableException
from com.aspose.slides import AxesManager
from com.aspose.slides import Axis
from com.aspose.slides import AxisAggregationType
from com.aspose.slides import AxisFormat
from com.aspose.slides import AxisPositionType
from com.aspose.slides import Backdrop3DScene
from com.aspose.slides import Background
from com.aspose.slides import BackgroundType
from com.aspose.slides import BaseChartValue
from com.aspose.slides import BaseHandoutNotesSlideHeaderFooterManager
from com.aspose.slides import BaseHeaderFooterManager
from com.aspose.slides import BaseOverrideThemeManager
from com.aspose.slides import BasePortionFormat
from com.aspose.slides import BaseScript
from com.aspose.slides import BaseShapeLock
from com.aspose.slides import BaseSlide
from com.aspose.slides import BaseSlideHeaderFooterManager
from com.aspose.slides import BaseThemeManager
from com.aspose.slides import Behavior
from com.aspose.slides import BehaviorAccumulateType
from com.aspose.slides import BehaviorAdditiveType
from com.aspose.slides import BehaviorCollection
from com.aspose.slides import BehaviorFactory
from com.aspose.slides import BehaviorProperty
from com.aspose.slides import BehaviorPropertyCollection
from com.aspose.slides import BevelPresetType
from com.aspose.slides import BiLevel
from com.aspose.slides import BlackWhiteConversionMode
from com.aspose.slides import BlackWhiteMode
from com.aspose.slides import BlobManagementOptions
from com.aspose.slides import Blur
from com.aspose.slides import BrowsedAtKiosk
from com.aspose.slides import BrowsedByIndividual
from com.aspose.slides import BubbleSizeRepresentationType
from com.aspose.slides import BuildType
from com.aspose.slides import BulletFormat
from com.aspose.slides import BulletType
from com.aspose.slides import Camera
from com.aspose.slides import CameraPresetType
from com.aspose.slides import CannotCombine2DAnd3DChartsException
from com.aspose.slides import CategoryAxisType
from com.aspose.slides import Cell
from com.aspose.slides import CellCircularReferenceException
from com.aspose.slides import CellCollection
from com.aspose.slides import CellFormat
from com.aspose.slides import CellInvalidFormulaException
from com.aspose.slides import CellInvalidReferenceException
from com.aspose.slides import CellUnsupportedDataException
from com.aspose.slides import Chart
@JImplementationFor("com.aspose.slides.Chart")
class _Chart(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import ChartCategory
from com.aspose.slides import ChartCategoryCollection
from com.aspose.slides import ChartCategoryLevelsManager
from com.aspose.slides import ChartCellCollection
from com.aspose.slides import ChartData
from com.aspose.slides import ChartDataCell
from com.aspose.slides import ChartDataPoint
from com.aspose.slides import ChartDataPointCollection
from com.aspose.slides import ChartDataPointLevel
from com.aspose.slides import ChartDataPointLevelsManager
from com.aspose.slides import ChartDataSourceType
from com.aspose.slides import ChartDataWorkbook
from com.aspose.slides import ChartDataWorksheet
from com.aspose.slides import ChartDataWorksheetCollection
from com.aspose.slides import ChartLinesFormat
from com.aspose.slides import ChartPlotArea
from com.aspose.slides import ChartPortionFormat
from com.aspose.slides import ChartSeries
from com.aspose.slides import ChartSeriesCollection
from com.aspose.slides import ChartSeriesGroup
from com.aspose.slides import ChartShapeType
from com.aspose.slides import ChartTextFormat
from com.aspose.slides import ChartThemeManager
from com.aspose.slides import ChartTitle
from com.aspose.slides import ChartType
from com.aspose.slides import ChartTypeCharacterizer
from com.aspose.slides import ChartWall
from com.aspose.slides import Collect
from com.aspose.slides import ColorChange
from com.aspose.slides import ColorDirection
from com.aspose.slides import ColorEffect
from com.aspose.slides import ColorFormat
from com.aspose.slides import ColorOffset
from com.aspose.slides import ColorOperation
from com.aspose.slides import ColorOperationCollection
from com.aspose.slides import ColorReplace
from com.aspose.slides import ColorScheme
from com.aspose.slides import ColorSchemeIndex
from com.aspose.slides import ColorSpace
from com.aspose.slides import ColorStringFormat
from com.aspose.slides import ColorTransformOperation
from com.aspose.slides import ColorType
from com.aspose.slides import Column
from com.aspose.slides import ColumnCollection
from com.aspose.slides import ColumnFormat
from com.aspose.slides import CombinableSeriesTypesGroup
from com.aspose.slides import CommandEffect
from com.aspose.slides import CommandEffectType
from com.aspose.slides import Comment
from com.aspose.slides import CommentAuthor
from com.aspose.slides import CommentAuthorCollection
from com.aspose.slides import CommentCollection
from com.aspose.slides import CommentsPositions
from com.aspose.slides import CommonSlideViewProperties
from com.aspose.slides import Compress
from com.aspose.slides import Conformance
from com.aspose.slides import Connector
@JImplementationFor("com.aspose.slides.Connector")
class _Connector(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import ConnectorLock
from com.aspose.slides import Control
from com.aspose.slides import ControlCollection
from com.aspose.slides import ControlPropertiesCollection
from com.aspose.slides import ControlType
from com.aspose.slides import Convert
from com.aspose.slides import CornerDirectionTransition
from com.aspose.slides import CrossesType
from com.aspose.slides import CurrentThreadSettings
from com.aspose.slides import CustomData
from com.aspose.slides import CustomXmlPart
from com.aspose.slides import CustomXmlPartCollection
@JImplementationFor("com.aspose.slides.CustomXmlPartCollection")
class _CustomXmlPartCollection(object):
	def addFromBytes(self, *args):
		if len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.add(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import DataLabel
from com.aspose.slides import DataLabelCollection
from com.aspose.slides import DataLabelFormat
from com.aspose.slides import DataSourceType
from com.aspose.slides import DataSourceTypeForErrorBarsCustomValues
from com.aspose.slides import DataTable
from com.aspose.slides import DigitalSignature
from com.aspose.slides import DigitalSignatureCollection
from com.aspose.slides import DisplayBlanksAsType
from com.aspose.slides import DisplayUnitType
from com.aspose.slides import DocumentProperties
from com.aspose.slides import DomObject
from com.aspose.slides import DoubleChartValue
from com.aspose.slides import Duotone
from com.aspose.slides import Effect
from com.aspose.slides import EffectChartMajorGroupingType
from com.aspose.slides import EffectChartMinorGroupingType
from com.aspose.slides import EffectFactory
from com.aspose.slides import EffectFillType
from com.aspose.slides import EffectFormat
from com.aspose.slides import EffectPresetClassType
from com.aspose.slides import EffectRestartType
from com.aspose.slides import EffectStyle
from com.aspose.slides import EffectStyleCollection
from com.aspose.slides import EffectSubtype
from com.aspose.slides import EffectTriggerType
from com.aspose.slides import EffectType
from com.aspose.slides import EightDirectionTransition
from com.aspose.slides import EmbedAllFontsHtmlController
from com.aspose.slides import EmbedFontCharacters
from com.aspose.slides import EmbeddedEotFontsHtmlController
from com.aspose.slides import EmbeddedWoffFontsHtmlController
from com.aspose.slides import EmptyTransition
from com.aspose.slides import ErrorBarType
from com.aspose.slides import ErrorBarValueType
from com.aspose.slides import ErrorBarsCustomValues
from com.aspose.slides import ErrorBarsFormat
from com.aspose.slides import ExternalResourceResolver
from com.aspose.slides import ExtraColorScheme
from com.aspose.slides import ExtraColorSchemeCollection
from com.aspose.slides import Field
from com.aspose.slides import FieldType
from com.aspose.slides import FillBlendMode
from com.aspose.slides import FillFormat
from com.aspose.slides import FillFormatCollection
from com.aspose.slides import FillOverlay
from com.aspose.slides import FillType
from com.aspose.slides import FilterEffect
from com.aspose.slides import FilterEffectRevealType
from com.aspose.slides import FilterEffectSubtype
from com.aspose.slides import FilterEffectType
from com.aspose.slides import Flavor
from com.aspose.slides import FlyThroughTransition
from com.aspose.slides import FontAlignment
from com.aspose.slides import FontCollectionIndex
from com.aspose.slides import FontData
from com.aspose.slides import FontDataFactory
from com.aspose.slides import FontFallBackRule
from com.aspose.slides import FontFallBackRulesCollection
from com.aspose.slides import FontScheme
from com.aspose.slides import FontSources
from com.aspose.slides import FontSubstCondition
from com.aspose.slides import FontSubstRule
from com.aspose.slides import FontSubstRuleCollection
from com.aspose.slides import FontSubstitutionInfo
from com.aspose.slides import Fonts
from com.aspose.slides import FontsLoader
from com.aspose.slides import FontsManager
from com.aspose.slides import ForEach
from com.aspose.slides import Format
from com.aspose.slides import FormatFactory
from com.aspose.slides import FormatScheme
from com.aspose.slides import FrameTickEventArgs
from com.aspose.slides import GeometryPath
from com.aspose.slides import GeometryShape
@JImplementationFor("com.aspose.slides.GeometryShape")
class _GeometryShape(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import GifOptions
from com.aspose.slides import GlitterTransition
from com.aspose.slides import GlobalLayoutSlideCollection
from com.aspose.slides import Glow
from com.aspose.slides import GradientDirection
from com.aspose.slides import GradientFormat
from com.aspose.slides import GradientShape
from com.aspose.slides import GradientStop
from com.aspose.slides import GradientStopCollection
from com.aspose.slides import GradientStopCollectionEffectiveData
from com.aspose.slides import GradientStopEffectiveData
from com.aspose.slides import GradientStyle
from com.aspose.slides import GraphicalObject
@JImplementationFor("com.aspose.slides.GraphicalObject")
class _GraphicalObject(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import GraphicalObjectLock
from com.aspose.slides import GrayScale
from com.aspose.slides import GroupShape
@JImplementationFor("com.aspose.slides.GroupShape")
class _GroupShape(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import GroupShapeLock
from com.aspose.slides import HSL
from com.aspose.slides import HandoutLayoutingOptions
from com.aspose.slides import HandoutType
from com.aspose.slides import Html5Options
from com.aspose.slides import HtmlExternalResolver
from com.aspose.slides import HtmlFormatter
from com.aspose.slides import HtmlGenerator
from com.aspose.slides import HtmlOptions
from com.aspose.slides import Hyperlink
from com.aspose.slides import HyperlinkActionType
from com.aspose.slides import HyperlinkColorSource
from com.aspose.slides import HyperlinkManager
from com.aspose.slides import HyperlinkQueries
from com.aspose.slides import ImageCollection
@JImplementationFor("com.aspose.slides.ImageCollection")
class _ImageCollection(object):
	def addImageFromBytes(self, *args):
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addImage(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addImage(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import ImageFormat
from com.aspose.slides import ImagePixelFormat
from com.aspose.slides import ImageTransformOCollectionEffectiveData
from com.aspose.slides import ImageTransformOperation
from com.aspose.slides import ImageTransformOperationCollection
from com.aspose.slides import ImageTransformOperationFactory
from com.aspose.slides import Images
@JImplementationFor("com.aspose.slides.Images")
class _Images(object):
	@staticmethod
	def fromStreamFromBytes(*args):
		if len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return Images.fromStream(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import InOutTransition
from com.aspose.slides import Ink
@JImplementationFor("com.aspose.slides.Ink")
class _Ink(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import InkBrush
from com.aspose.slides import InkOptions
from com.aspose.slides import InkTrace
from com.aspose.slides import InnerShadow
from com.aspose.slides import Input
from com.aspose.slides import InterruptionToken
from com.aspose.slides import InterruptionTokenSource
from com.aspose.slides import InvalidPasswordException
from com.aspose.slides import LayoutSlide
from com.aspose.slides import LayoutSlideCollection
from com.aspose.slides import LayoutSlideHeaderFooterManager
from com.aspose.slides import LayoutSlideThemeManager
from com.aspose.slides import LayoutTargetType
from com.aspose.slides import LeftRightDirectionTransition
from com.aspose.slides import LegacyDiagram
@JImplementationFor("com.aspose.slides.LegacyDiagram")
class _LegacyDiagram(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import Legend
from com.aspose.slides import LegendDataLabelPosition
from com.aspose.slides import LegendEntryCollection
from com.aspose.slides import LegendEntryProperties
from com.aspose.slides import LegendPositionType
from com.aspose.slides import License
@JImplementationFor("com.aspose.slides.License")
class _License(object):
	def setLicenseFromBytes(self, *args):
		if len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.setLicense(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import LightRig
from com.aspose.slides import LightRigPresetType
from com.aspose.slides import LightingDirection
from com.aspose.slides import LineAlignment
from com.aspose.slides import LineArrowheadLength
from com.aspose.slides import LineArrowheadStyle
from com.aspose.slides import LineArrowheadWidth
from com.aspose.slides import LineCapStyle
from com.aspose.slides import LineDashStyle
from com.aspose.slides import LineFillFormat
from com.aspose.slides import LineFormat
from com.aspose.slides import LineFormatCollection
from com.aspose.slides import LineJoinStyle
from com.aspose.slides import LineSketchType
from com.aspose.slides import LineStyle
from com.aspose.slides import LinkEmbedDecision
from com.aspose.slides import LoadFormat
from com.aspose.slides import LoadOptions
from com.aspose.slides import LoadingStreamBehavior
from com.aspose.slides import Luminance
from com.aspose.slides import MarkdownExportType
from com.aspose.slides import MarkdownSaveOptions
from com.aspose.slides import Marker
from com.aspose.slides import MarkerStyleType
from com.aspose.slides import MasterHandoutSlide
from com.aspose.slides import MasterHandoutSlideHeaderFooterManager
from com.aspose.slides import MasterLayoutSlideCollection
from com.aspose.slides import MasterNotesSlide
from com.aspose.slides import MasterNotesSlideHeaderFooterManager
from com.aspose.slides import MasterSlide
from com.aspose.slides import MasterSlideCollection
from com.aspose.slides import MasterSlideHeaderFooterManager
from com.aspose.slides import MasterTheme
from com.aspose.slides import MasterThemeManager
from com.aspose.slides import MaterialPresetType
from com.aspose.slides import MathAccent
from com.aspose.slides import MathAccentFactory
from com.aspose.slides import MathArray
from com.aspose.slides import MathArrayFactory
from com.aspose.slides import MathBar
from com.aspose.slides import MathBarFactory
from com.aspose.slides import MathBlock
@JImplementationFor("com.aspose.slides.MathBlock")
class _MathBlock(object):
	def writeAsMathMlToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 0:
			self.writeAsMathMl(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import MathBlockFactory
from com.aspose.slides import MathBorderBox
from com.aspose.slides import MathBorderBoxFactory
from com.aspose.slides import MathBox
from com.aspose.slides import MathBoxFactory
from com.aspose.slides import MathDelimiter
from com.aspose.slides import MathDelimiterFactory
from com.aspose.slides import MathDelimiterShape
from com.aspose.slides import MathElementBase
from com.aspose.slides import MathFraction
from com.aspose.slides import MathFractionFactory
from com.aspose.slides import MathFractionTypes
from com.aspose.slides import MathFunction
from com.aspose.slides import MathFunctionFactory
from com.aspose.slides import MathFunctionsOfOneArgument
from com.aspose.slides import MathFunctionsOfTwoArguments
from com.aspose.slides import MathGroupingCharacter
from com.aspose.slides import MathGroupingCharacterFactory
from com.aspose.slides import MathHorizontalAlignment
from com.aspose.slides import MathIntegralTypes
from com.aspose.slides import MathJustification
from com.aspose.slides import MathLeftSubSuperscriptElement
from com.aspose.slides import MathLimit
from com.aspose.slides import MathLimitFactory
from com.aspose.slides import MathLimitLocations
from com.aspose.slides import MathMatrix
from com.aspose.slides import MathMatrixFactory
from com.aspose.slides import MathNaryOperator
from com.aspose.slides import MathNaryOperatorFactory
from com.aspose.slides import MathNaryOperatorTypes
from com.aspose.slides import MathParagraph
@JImplementationFor("com.aspose.slides.MathParagraph")
class _MathParagraph(object):
	def writeAsMathMlToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 0:
			self.writeAsMathMl(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import MathParagraphFactory
from com.aspose.slides import MathPortion
from com.aspose.slides import MathRadical
from com.aspose.slides import MathRadicalFactory
from com.aspose.slides import MathRightSubSuperscriptElement
from com.aspose.slides import MathRightSubSuperscriptElementFactory
from com.aspose.slides import MathRowSpacingRule
from com.aspose.slides import MathSpacingRules
from com.aspose.slides import MathSubscriptElement
from com.aspose.slides import MathSubscriptElementFactory
from com.aspose.slides import MathSuperscriptElement
from com.aspose.slides import MathSuperscriptElementFactory
from com.aspose.slides import MathTopBotPositions
from com.aspose.slides import MathVerticalAlignment
from com.aspose.slides import MathematicalText
from com.aspose.slides import MathematicalTextFactory
from com.aspose.slides import Metered
from com.aspose.slides import ModernComment
from com.aspose.slides import ModernCommentStatus
from com.aspose.slides import MorphTransition
from com.aspose.slides import MotionCmdPath
from com.aspose.slides import MotionCommandPathType
from com.aspose.slides import MotionEffect
from com.aspose.slides import MotionOriginType
from com.aspose.slides import MotionPath
from com.aspose.slides import MotionPathEditMode
from com.aspose.slides import MotionPathPointsType
from com.aspose.slides import NewLineType
from com.aspose.slides import NormalViewProperties
from com.aspose.slides import NormalViewRestoredProperties
from com.aspose.slides import NotesCommentsLayoutingOptions
from com.aspose.slides import NotesPositions
from com.aspose.slides import NotesSize
from com.aspose.slides import NotesSlide
from com.aspose.slides import NotesSlideHeaderFooterManager
from com.aspose.slides import NotesSlideManager
from com.aspose.slides import NotesSlideThemeManager
from com.aspose.slides import NullableBool
from com.aspose.slides import NumberedBulletStyle
from com.aspose.slides import OOXMLCorruptFileException
from com.aspose.slides import OOXMLException
from com.aspose.slides import OdpException
from com.aspose.slides import OdpReadException
from com.aspose.slides import OleEmbeddedDataInfo
from com.aspose.slides import OleObjectFrame
@JImplementationFor("com.aspose.slides.OleObjectFrame")
class _OleObjectFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import OptionalBlackTransition
from com.aspose.slides import OrganizationChartLayoutType
from com.aspose.slides import Orientation
from com.aspose.slides import OrientationTransition
from com.aspose.slides import OuterShadow
from com.aspose.slides import Output
from com.aspose.slides import OutputFile
@JImplementationFor("com.aspose.slides.OutputFile")
class _OutputFile(object):
	def writeToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 0:
			self.write(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import OverrideTheme
from com.aspose.slides import PPImage
from com.aspose.slides import PVIObject
from com.aspose.slides import Paragraph
from com.aspose.slides import ParagraphCollection
from com.aspose.slides import ParagraphFactory
from com.aspose.slides import ParagraphFormat
from com.aspose.slides import ParentLabelLayoutType
from com.aspose.slides import PathCommandType
from com.aspose.slides import PathFillModeType
from com.aspose.slides import PathSegment
from com.aspose.slides import PatternFormat
from com.aspose.slides import PatternStyle
from com.aspose.slides import PdfAccessPermissions
from com.aspose.slides import PdfCompliance
from com.aspose.slides import PdfImportOptions
from com.aspose.slides import PdfOptions
from com.aspose.slides import PdfTextCompression
from com.aspose.slides import PersistenceType
from com.aspose.slides import Picture
from com.aspose.slides import PictureFillFormat
from com.aspose.slides import PictureFillMode
from com.aspose.slides import PictureFrame
@JImplementationFor("com.aspose.slides.PictureFrame")
class _PictureFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import PictureFrameLock
from com.aspose.slides import PictureType
from com.aspose.slides import PicturesCompression
from com.aspose.slides import PieSplitCustomPointCollection
from com.aspose.slides import PieSplitType
from com.aspose.slides import Placeholder
from com.aspose.slides import PlaceholderSize
from com.aspose.slides import PlaceholderType
from com.aspose.slides import Point
from com.aspose.slides import PointCollection
from com.aspose.slides import Portion
from com.aspose.slides import PortionCollection
from com.aspose.slides import PortionFactory
from com.aspose.slides import PortionFormat
from com.aspose.slides import PptCorruptFileException
from com.aspose.slides import PptEditException
from com.aspose.slides import PptException
from com.aspose.slides import PptOptions
from com.aspose.slides import PptReadException
from com.aspose.slides import PptUnsupportedFormatException
from com.aspose.slides import PptxCorruptFileException
from com.aspose.slides import PptxEditException
from com.aspose.slides import PptxException
from com.aspose.slides import PptxOptions
from com.aspose.slides import PptxReadException
from com.aspose.slides import PptxUnsupportedFormatException
from com.aspose.slides import Presentation
@JImplementationFor("com.aspose.slides.Presentation")
class _Presentation(object):
	@staticmethod
	def createPresentationFromBytes(*args):
		sb = StreamBuffer()
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb.write(args[0])
			return Presentation(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb.write(args[0])
			return Presentation(sb.toInputStream())
		raise ValueError("Invalid arguments")
	def saveToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 3:
			self.save(sb, args[0], args[1], args[2])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 2:
			self.save(sb, args[0], args[1])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 1:
			self.save(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import PresentationAnimationsGenerator
from com.aspose.slides import PresentationFactory
@JImplementationFor("com.aspose.slides.PresentationFactory")
class _PresentationFactory(object):
	def readPresentationFromBytes(self, *args):
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.readPresentation(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.readPresentation(sb.toInputStream())
		raise ValueError("Invalid arguments")
	def getPresentationInfoFromBytes(self, *args):
		if len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.getPresentationInfo(sb.toInputStream())
		raise ValueError("Invalid arguments")
	def getPresentationTextFromBytes(self, *args):
		if len(args) == 3 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.getPresentationText(sb.toInputStream(), args[1], args[2])
		elif len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.getPresentationText(sb.toInputStream(), args[1])
		raise ValueError("Invalid arguments")

from com.aspose.slides import PresentationHeaderFooterManager
from com.aspose.slides import PresentationInfo
@JImplementationFor("com.aspose.slides.PresentationInfo")
class _PresentationInfo(object):
	def writeBindedPresentationToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 0:
			self.writeBindedPresentation(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import PresentationLockingBehavior
from com.aspose.slides import PresentationPlayer
from com.aspose.slides import PresentationText
from com.aspose.slides import PresentedBySpeaker
from com.aspose.slides import PresetColor
from com.aspose.slides import PresetShadow
from com.aspose.slides import PresetShadowType
from com.aspose.slides import PropertyCalcModeType
from com.aspose.slides import PropertyEffect
from com.aspose.slides import PropertyValueType
from com.aspose.slides import ProtectionManager
from com.aspose.slides import QuartileMethodType
from com.aspose.slides import RectangleAlignment
from com.aspose.slides import Reflection
from com.aspose.slides import RenderingOptions
from com.aspose.slides import ResourceLoadingAction
from com.aspose.slides import ResponsiveHtmlController
from com.aspose.slides import ReturnAction
from com.aspose.slides import RevealTransition
from com.aspose.slides import RippleTransition
from com.aspose.slides import Rotation3D
from com.aspose.slides import RotationEffect
from com.aspose.slides import Row
from com.aspose.slides import RowCollection
from com.aspose.slides import RowFormat
from com.aspose.slides import SVGOptions
from com.aspose.slides import SaveFormat
from com.aspose.slides import SaveOptions
from com.aspose.slides import SaveOptionsFactory
from com.aspose.slides import ScaleEffect
from com.aspose.slides import SchemeColor
from com.aspose.slides import Section
from com.aspose.slides import SectionCollection
from com.aspose.slides import SectionSlideCollection
from com.aspose.slides import SectionZoomFrame
@JImplementationFor("com.aspose.slides.SectionZoomFrame")
class _SectionZoomFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import Sequence
from com.aspose.slides import SequenceCollection
from com.aspose.slides import SetEffect
from com.aspose.slides import Shape
@JImplementationFor("com.aspose.slides.Shape")
class _Shape(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import ShapeBevel
from com.aspose.slides import ShapeCollection
@JImplementationFor("com.aspose.slides.ShapeCollection")
class _ShapeCollection(object):
	def insertAudioFrameEmbeddedFromBytes(self, *args):
		if len(args) == 6 and args[5].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[5])
			return self.insertAudioFrameEmbedded(args[0], args[1], args[2], args[3], args[4], sb.toInputStream())
		raise ValueError("Invalid arguments")
	def addAudioFrameEmbeddedFromBytes(self, *args):
		if len(args) == 5 and args[4].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[4])
			return self.addAudioFrameEmbedded(args[0], args[1], args[2], args[3], sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import ShapeElement
from com.aspose.slides import ShapeElementFillSource
from com.aspose.slides import ShapeElementStrokeSource
from com.aspose.slides import ShapeFrame
from com.aspose.slides import ShapeStyle
from com.aspose.slides import ShapeThumbnailBounds
from com.aspose.slides import ShapeType
from com.aspose.slides import ShapeUtil
from com.aspose.slides import ShapesAlignmentType
from com.aspose.slides import ShredTransition
from com.aspose.slides import SideDirectionTransition
from com.aspose.slides import SketchFormat
from com.aspose.slides import Slide
@JImplementationFor("com.aspose.slides.Slide")
class _Slide(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import SlideCollection
@JImplementationFor("com.aspose.slides.SlideCollection")
class _SlideCollection(object):
	def insertFromHtmlFromBytes(self, *args):
		if len(args) == 4 and args[1].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[1])
			return self.insertFromHtml(args[0], sb.toInputStream(), args[2], args[3])
		elif len(args) == 2 and args[1].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[1])
			return self.insertFromHtml(args[0], sb.toInputStream())
		raise ValueError("Invalid arguments")
	def addFromPdfFromBytes(self, *args):
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addFromPdf(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addFromPdf(sb.toInputStream())
		raise ValueError("Invalid arguments")
	def addFromHtmlFromBytes(self, *args):
		if len(args) == 3 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addFromHtml(sb.toInputStream(), args[1], args[2])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addFromHtml(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import SlideHeaderFooterManager
from com.aspose.slides import SlideImageFormat
from com.aspose.slides import SlideLayoutType
from com.aspose.slides import SlideOrientation
from com.aspose.slides import SlideShowSettings
from com.aspose.slides import SlideShowTransition
from com.aspose.slides import SlideShowType
from com.aspose.slides import SlideSize
from com.aspose.slides import SlideSizeScaleType
from com.aspose.slides import SlideSizeType
from com.aspose.slides import SlideThemeManager
from com.aspose.slides import SlideUtil
from com.aspose.slides import SlidesRange
from com.aspose.slides import SmartArt
@JImplementationFor("com.aspose.slides.SmartArt")
class _SmartArt(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import SmartArtColorType
from com.aspose.slides import SmartArtLayoutType
from com.aspose.slides import SmartArtNode
from com.aspose.slides import SmartArtNodeCollection
from com.aspose.slides import SmartArtQuickStyleType
from com.aspose.slides import SmartArtShape
@JImplementationFor("com.aspose.slides.SmartArtShape")
class _SmartArtShape(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import SmartArtShapeCollection
from com.aspose.slides import SoftEdge
from com.aspose.slides import SourceFormat
from com.aspose.slides import SplitTransition
from com.aspose.slides import SplitterBarStateType
from com.aspose.slides import SpreadsheetOptions
from com.aspose.slides import Storage
from com.aspose.slides import StringChartValue
from com.aspose.slides import StringOrDoubleChartValue
from com.aspose.slides import StyleType
from com.aspose.slides import SummaryZoomFrame
@JImplementationFor("com.aspose.slides.SummaryZoomFrame")
class _SummaryZoomFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import SummaryZoomSection
@JImplementationFor("com.aspose.slides.SummaryZoomSection")
class _SummaryZoomSection(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import SummaryZoomSectionCollection
from com.aspose.slides import SvgCoordinateUnit
from com.aspose.slides import SvgEvent
from com.aspose.slides import SvgExternalFontsHandling
from com.aspose.slides import SvgImage
@JImplementationFor("com.aspose.slides.SvgImage")
class _SvgImage(object):
	@staticmethod
	def createSvgImageFromBytes(*args):
		sb = StreamBuffer()
		if len(args) == 3 and args[0].__class__.__name__ == 'bytes':
			sb.write(args[0])
			return SvgImage(sb.toInputStream(), args[1], args[2])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb.write(args[0])
			return SvgImage(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import SvgShape
from com.aspose.slides import SvgTSpan
from com.aspose.slides import SwfOptions
from com.aspose.slides import SystemColor
from com.aspose.slides import Tab
from com.aspose.slides import TabAlignment
from com.aspose.slides import TabCollection
from com.aspose.slides import TabFactory
from com.aspose.slides import Table
@JImplementationFor("com.aspose.slides.Table")
class _Table(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import TableFormat
from com.aspose.slides import TableStylePreset
from com.aspose.slides import TagCollection
from com.aspose.slides import TemplateContext
from com.aspose.slides import TextAlignment
from com.aspose.slides import TextAnchorType
from com.aspose.slides import TextAnimation
from com.aspose.slides import TextAnimationCollection
from com.aspose.slides import TextAutofitType
from com.aspose.slides import TextCapType
from com.aspose.slides import TextExtractionArrangingMode
from com.aspose.slides import TextFrame
from com.aspose.slides import TextFrameFormat
from com.aspose.slides import TextHighlightingOptions
from com.aspose.slides import TextInheritanceLimit
from com.aspose.slides import TextSearchOptions
from com.aspose.slides import TextShapeType
from com.aspose.slides import TextStrikethroughType
from com.aspose.slides import TextStyle
from com.aspose.slides import TextToHtmlConversionOptions
from com.aspose.slides import TextUnderlineType
from com.aspose.slides import TextVerticalOverflowType
from com.aspose.slides import TextVerticalType
from com.aspose.slides import Theme
from com.aspose.slides import ThreeDFormat
from com.aspose.slides import TickLabelPositionType
from com.aspose.slides import TickMarkType
from com.aspose.slides import TiffCompressionTypes
from com.aspose.slides import TiffOptions
from com.aspose.slides import TileFlip
from com.aspose.slides import TimeUnitType
from com.aspose.slides import Timing
from com.aspose.slides import Tint
from com.aspose.slides import TransitionCornerAndCenterDirectionType
from com.aspose.slides import TransitionCornerDirectionType
from com.aspose.slides import TransitionEightDirectionType
from com.aspose.slides import TransitionInOutDirectionType
from com.aspose.slides import TransitionLeftRightDirectionType
from com.aspose.slides import TransitionMorphType
from com.aspose.slides import TransitionPattern
from com.aspose.slides import TransitionShredPattern
from com.aspose.slides import TransitionSideDirectionType
from com.aspose.slides import TransitionSoundMode
from com.aspose.slides import TransitionSpeed
from com.aspose.slides import TransitionType
from com.aspose.slides import TransitionValueBase
from com.aspose.slides import Trendline
from com.aspose.slides import TrendlineCollection
from com.aspose.slides import TrendlineType
from com.aspose.slides import UpDownBarsManager
from com.aspose.slides import VbaModule
from com.aspose.slides import VbaModuleCollection
from com.aspose.slides import VbaProject
from com.aspose.slides import VbaProjectFactory
from com.aspose.slides import VbaReferenceCollection
from com.aspose.slides import VbaReferenceFactory
from com.aspose.slides import VbaReferenceOleTypeLib
from com.aspose.slides import Video
from com.aspose.slides import VideoCollection
@JImplementationFor("com.aspose.slides.VideoCollection")
class _VideoCollection(object):
	def addVideoFromBytes(self, *args):
		if len(args) == 2 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addVideo(sb.toInputStream(), args[1])
		elif len(args) == 1 and args[0].__class__.__name__ == 'bytes':
			sb = StreamBuffer()
			sb.write(args[0])
			return self.addVideo(sb.toInputStream())
		raise ValueError("Invalid arguments")

from com.aspose.slides import VideoFrame
@JImplementationFor("com.aspose.slides.VideoFrame")
class _VideoFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import VideoPlayModePreset
from com.aspose.slides import VideoPlayerHtmlController
from com.aspose.slides import VideoPlayerHtmlControllerFactory
from com.aspose.slides import ViewProperties
from com.aspose.slides import ViewType
from com.aspose.slides import WarningType
from com.aspose.slides import WebDocument
from com.aspose.slides import WebDocumentOptions
from com.aspose.slides import WheelTransition
from com.aspose.slides import XamlOptions
from com.aspose.slides import XpsOptions
from com.aspose.slides import Zip64Mode
from com.aspose.slides import ZoomFrame
@JImplementationFor("com.aspose.slides.ZoomFrame")
class _ZoomFrame(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

from com.aspose.slides import ZoomImageType
from com.aspose.slides import ZoomLayout
from com.aspose.slides import ZoomObject
@JImplementationFor("com.aspose.slides.ZoomObject")
class _ZoomObject(object):
	def writeAsSvgToBytes(self, *args):
		sb = StreamBuffer()
		if len(args) == 1:
			self.writeAsSvg(sb, args[0])
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		elif len(args) == 0:
			self.writeAsSvg(sb)
			buf = sb.toByteArray()
			return array("b", buf).tobytes()
		raise ValueError("Invalid arguments")

