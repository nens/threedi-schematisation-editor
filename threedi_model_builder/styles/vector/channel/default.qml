<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" minScale="0" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" version="3.16.3-Hannover" labelsEnabled="0" readOnly="0" hasScaleBasedVisibilityFlag="0" maxScale="0" styleCategories="AllStyleCategories" simplifyDrawingHints="1">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal enabled="0" accumulate="0" startField="" fixedDuration="0" mode="0" startExpression="" durationUnit="min" endField="" endExpression="" durationField="">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 forceraster="0" symbollevels="0" type="singleSymbol" enableorderby="0">
    <symbols>
      <symbol alpha="1" force_rhr="0" type="line" name="0" clip_to_extent="1">
        <layer class="SimpleLine" enabled="1" pass="0" locked="0">
          <prop v="0" k="align_dash_pattern"/>
          <prop v="square" k="capstyle"/>
          <prop v="5;2" k="customdash"/>
          <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
          <prop v="MM" k="customdash_unit"/>
          <prop v="0" k="dash_pattern_offset"/>
          <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
          <prop v="MM" k="dash_pattern_offset_unit"/>
          <prop v="0" k="draw_inside_polygon"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="5,77,209,255" k="line_color"/>
          <prop v="solid" k="line_style"/>
          <prop v="0.66" k="line_width"/>
          <prop v="MM" k="line_width_unit"/>
          <prop v="0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0" k="ring_filter"/>
          <prop v="0" k="tweak_dash_pattern_on_corners"/>
          <prop v="0" k="use_custom_dash"/>
          <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="outlineWidth">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 0.66,0.3)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer diagramType="Histogram" attributeLegend="1">
    <DiagramCategory direction="0" sizeScale="3x:0,0,0,0,0,0" rotationOffset="270" width="15" backgroundAlpha="255" penAlpha="255" barWidth="5" spacing="5" enabled="0" height="15" minScaleDenominator="0" lineSizeType="MM" maxScaleDenominator="0" penWidth="0" lineSizeScale="3x:0,0,0,0,0,0" scaleBasedVisibility="0" spacingUnitScale="3x:0,0,0,0,0,0" opacity="1" labelPlacementMethod="XHeight" backgroundColor="#ffffff" showAxis="1" diagramOrientation="Up" minimumSize="0" spacingUnit="MM" sizeType="MM" scaleDependency="Area" penColor="#000000">
      <fontProperties style="" description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0"/>
      <axisSymbol>
        <symbol alpha="1" force_rhr="0" type="line" name="" clip_to_extent="1">
          <layer class="SimpleLine" enabled="1" pass="0" locked="0">
            <prop v="0" k="align_dash_pattern"/>
            <prop v="square" k="capstyle"/>
            <prop v="5;2" k="customdash"/>
            <prop v="3x:0,0,0,0,0,0" k="customdash_map_unit_scale"/>
            <prop v="MM" k="customdash_unit"/>
            <prop v="0" k="dash_pattern_offset"/>
            <prop v="3x:0,0,0,0,0,0" k="dash_pattern_offset_map_unit_scale"/>
            <prop v="MM" k="dash_pattern_offset_unit"/>
            <prop v="0" k="draw_inside_polygon"/>
            <prop v="bevel" k="joinstyle"/>
            <prop v="35,35,35,255" k="line_color"/>
            <prop v="solid" k="line_style"/>
            <prop v="0.26" k="line_width"/>
            <prop v="MM" k="line_width_unit"/>
            <prop v="0" k="offset"/>
            <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
            <prop v="MM" k="offset_unit"/>
            <prop v="0" k="ring_filter"/>
            <prop v="0" k="tweak_dash_pattern_on_corners"/>
            <prop v="0" k="use_custom_dash"/>
            <prop v="3x:0,0,0,0,0,0" k="width_map_unit_scale"/>
            <data_defined_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" dist="0" obstacle="0" placement="2" zIndex="0" priority="0">
    <properties>
      <Option type="Map">
        <Option value="" type="QString" name="name"/>
        <Option name="properties"/>
        <Option value="collection" type="QString" name="type"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions removeDuplicateNodes="0" geometryPrecision="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="calculation_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="100" type="QString" name="100: embedded"/>
              </Option>
              <Option type="Map">
                <Option value="101" type="QString" name="101: isolated"/>
              </Option>
              <Option type="Map">
                <Option value="102" type="QString" name="102: connected"/>
              </Option>
              <Option type="Map">
                <Option value="105" type="QString" name="105: double connected"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dist_calc_points" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="-1" type="QString" name="-1"/>
              </Option>
              <Option type="Map">
                <Option value="0" type="QString" name="0"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3"/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_start_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="connection_node_end_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="code" index="2" name=""/>
    <alias field="display_name" index="3" name=""/>
    <alias field="calculation_type" index="4" name=""/>
    <alias field="dist_calc_points" index="5" name=""/>
    <alias field="zoom_category" index="6" name=""/>
    <alias field="connection_node_start_id" index="7" name=""/>
    <alias field="connection_node_end_id" index="8" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="'new'" applyOnUpdate="0" field="display_name"/>
    <default expression="" applyOnUpdate="0" field="calculation_type"/>
    <default expression="" applyOnUpdate="0" field="dist_calc_points"/>
    <default expression="5" applyOnUpdate="0" field="zoom_category"/>
    <default expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,start_point(geometry(@parent))))" applyOnUpdate="0" field="connection_node_start_id"/>
    <default expression="aggregate('v2_connection_nodes','min',&quot;id&quot;, intersects($geometry,end_point(geometry(@parent))))" applyOnUpdate="0" field="connection_node_end_id"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="code" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="display_name" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="calculation_type" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="dist_calc_points" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="zoom_category" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="connection_node_start_id" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="connection_node_end_id" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="display_name"/>
    <constraint exp="" desc="" field="calculation_type"/>
    <constraint exp="" desc="" field="dist_calc_points"/>
    <constraint exp="" desc="" field="zoom_category"/>
    <constraint exp="" desc="" field="connection_node_start_id"/>
    <constraint exp="" desc="" field="connection_node_end_id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="code"/>
      <column width="-1" hidden="0" type="field" name="display_name"/>
      <column width="-1" hidden="0" type="field" name="calculation_type"/>
      <column width="-1" hidden="0" type="field" name="dist_calc_points"/>
      <column width="-1" hidden="0" type="field" name="zoom_category"/>
      <column width="-1" hidden="0" type="field" name="connection_node_start_id"/>
      <column width="-1" hidden="0" type="field" name="connection_node_end_id"/>
      <column width="-1" hidden="1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">../../../OSGEO4~1/bin</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>../../../OSGEO4~1/bin</editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from PyQt4.QtGui import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Channel" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="General" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="3" name="display_name"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="4" name="calculation_type"/>
        <attributeEditorField showLabel="1" index="5" name="dist_calc_points"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Visualization" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="6" name="zoom_category"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Connection nodes" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="7" name="connection_node_start_id"/>
        <attributeEditorField showLabel="1" index="8" name="connection_node_end_id"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="calculation_type"/>
    <field editable="1" name="code"/>
    <field editable="1" name="connection_node_end_id"/>
    <field editable="1" name="connection_node_start_id"/>
    <field editable="1" name="display_name"/>
    <field editable="1" name="dist_calc_points"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="zoom_category"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="calculation_type"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="connection_node_end_id"/>
    <field labelOnTop="0" name="connection_node_start_id"/>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="dist_calc_points"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="zoom_category"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>1</layerGeometryType>
</qgis>
