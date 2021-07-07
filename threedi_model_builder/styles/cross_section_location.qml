<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" minScale="0" simplifyDrawingTol="1" simplifyLocal="1" simplifyMaxScale="1" version="3.16.3-Hannover" labelsEnabled="0" readOnly="0" hasScaleBasedVisibilityFlag="0" maxScale="0" styleCategories="AllStyleCategories" simplifyDrawingHints="0">
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
      <symbol alpha="1" force_rhr="0" type="marker" name="0" clip_to_extent="1">
        <layer class="SimpleMarker" enabled="1" pass="0" locked="0">
          <prop v="0" k="angle"/>
          <prop v="19,61,142,255" k="color"/>
          <prop v="1" k="horizontal_anchor_point"/>
          <prop v="bevel" k="joinstyle"/>
          <prop v="diamond" k="name"/>
          <prop v="0,0" k="offset"/>
          <prop v="3x:0,0,0,0,0,0" k="offset_map_unit_scale"/>
          <prop v="MM" k="offset_unit"/>
          <prop v="0,0,0,255" k="outline_color"/>
          <prop v="solid" k="outline_style"/>
          <prop v="0" k="outline_width"/>
          <prop v="3x:0,0,0,0,0,0" k="outline_width_map_unit_scale"/>
          <prop v="MM" k="outline_width_unit"/>
          <prop v="area" k="scale_method"/>
          <prop v="2" k="size"/>
          <prop v="3x:0,0,0,0,0,0" k="size_map_unit_scale"/>
          <prop v="MM" k="size_unit"/>
          <prop v="1" k="vertical_anchor_point"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="if(@map_scale&lt;10000, 2,0.5)" type="QString" name="expression"/>
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
  <DiagramLayerSettings linePlacementFlags="18" showAll="1" dist="0" obstacle="0" placement="0" zIndex="0" priority="0">
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
    <field name="reference_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_shape" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name="id"/>
    <alias field="code" index="2" name="code"/>
    <alias field="reference_level" index="3" name="reference_level"/>
    <alias field="friction_type" index="4" name="friction_type"/>
    <alias field="friction_value" index="5" name="friction_value"/>
    <alias field="bank_level" index="6" name="bank_level"/>
    <alias field="channel_id" index="7" name="channel_id"/>
    <alias field="cross_section_definition_id" index="8" name=""/>
    <alias field="cross_section_definition_code" index="9" name=""/>
    <alias field="cross_section_definition_width" index="10" name=""/>
    <alias field="cross_section_definition_height" index="11" name=""/>
    <alias field="cross_section_definition_shape" index="12" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1,maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="'new'" applyOnUpdate="0" field="code"/>
    <default expression="" applyOnUpdate="0" field="reference_level"/>
    <default expression="2" applyOnUpdate="0" field="friction_type"/>
    <default expression="" applyOnUpdate="0" field="friction_value"/>
    <default expression="" applyOnUpdate="0" field="bank_level"/>
    <default expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))" applyOnUpdate="0" field="channel_id"/>
    <default expression="" applyOnUpdate="0" field="cross_section_definition_id"/>
    <default expression="'new'" applyOnUpdate="0" field="cross_section_definition_code"/>
    <default expression="" applyOnUpdate="0" field="cross_section_definition_width"/>
    <default expression="" applyOnUpdate="0" field="cross_section_definition_height"/>
    <default expression="" applyOnUpdate="0" field="cross_section_definition_shape"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="code" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="reference_level" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="friction_type" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="friction_value" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="bank_level" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="channel_id" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="cross_section_definition_id" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="cross_section_definition_code" unique_strength="0"/>
    <constraint constraints="5" exp_strength="2" notnull_strength="2" field="cross_section_definition_width" unique_strength="0"/>
    <constraint constraints="4" exp_strength="2" notnull_strength="0" field="cross_section_definition_height" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="cross_section_definition_shape" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="reference_level"/>
    <constraint exp="" desc="" field="friction_type"/>
    <constraint exp="" desc="" field="friction_value"/>
    <constraint exp="" desc="" field="bank_level"/>
    <constraint exp="" desc="" field="channel_id"/>
    <constraint exp="" desc="" field="cross_section_definition_id"/>
    <constraint exp="" desc="" field="cross_section_definition_code"/>
    <constraint exp="regexp_match(&quot;width&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$')" desc="" field="cross_section_definition_width"/>
    <constraint exp="regexp_match(&quot;height&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$') or &quot;height&quot;is null" desc="" field="cross_section_definition_height"/>
    <constraint exp="" desc="" field="cross_section_definition_shape"/>
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
      <column width="-1" hidden="0" type="field" name="reference_level"/>
      <column width="-1" hidden="0" type="field" name="friction_type"/>
      <column width="-1" hidden="0" type="field" name="friction_value"/>
      <column width="-1" hidden="0" type="field" name="bank_level"/>
      <column width="-1" hidden="0" type="field" name="channel_id"/>
      <column width="-1" hidden="0" type="field" name="cross_section_definition_id"/>
      <column width="-1" hidden="1" type="actions"/>
      <column width="-1" hidden="0" type="field" name="cross_section_definition_code"/>
      <column width="-1" hidden="0" type="field" name="cross_section_definition_width"/>
      <column width="-1" hidden="0" type="field" name="cross_section_definition_height"/>
      <column width="-1" hidden="0" type="field" name="cross_section_definition_shape"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
  <editform tolerant="1">.</editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
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
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Cross section location view" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="General" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="reference_level"/>
        <attributeEditorField showLabel="1" index="6" name="bank_level"/>
        <attributeEditorField showLabel="1" index="4" name="friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="friction_value"/>
        <attributeEditorField showLabel="1" index="7" name="channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" columnCount="1" name="Cross section" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="8" name="cross_section_definition_id"/>
        <attributeEditorField showLabel="1" index="12" name="cross_section_definition_shape"/>
        <attributeEditorField showLabel="1" index="11" name="cross_section_definition_height"/>
        <attributeEditorField showLabel="1" index="10" name="cross_section_definition_width"/>
        <attributeEditorField showLabel="1" index="9" name="cross_section_definition_code"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="0" name="Cross section definition_code"/>
    <field editable="0" name="Cross section definition_height"/>
    <field editable="0" name="Cross section definition_shape"/>
    <field editable="0" name="Cross section definition_width"/>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="0" name="cross_section_definition_code"/>
    <field editable="0" name="cross_section_definition_height"/>
    <field editable="1" name="cross_section_definition_id"/>
    <field editable="0" name="cross_section_definition_shape"/>
    <field editable="0" name="cross_section_definition_width"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="location_bank_level"/>
    <field editable="1" name="location_channel_id"/>
    <field editable="1" name="location_code"/>
    <field editable="1" name="location_definition_id"/>
    <field editable="1" name="location_friction_type"/>
    <field editable="1" name="location_friction_value"/>
    <field editable="1" name="location_id"/>
    <field editable="1" name="location_reference_level"/>
    <field editable="1" name="reference_level"/>
    <field editable="0" name="v2_cross_section_definition_code"/>
    <field editable="0" name="v2_cross_section_definition_height"/>
    <field editable="0" name="v2_cross_section_definition_shape"/>
    <field editable="0" name="v2_cross_section_definition_width"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="Cross section definition_code"/>
    <field labelOnTop="0" name="Cross section definition_height"/>
    <field labelOnTop="0" name="Cross section definition_shape"/>
    <field labelOnTop="0" name="Cross section definition_width"/>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="cross_section_definition_code"/>
    <field labelOnTop="0" name="cross_section_definition_height"/>
    <field labelOnTop="0" name="cross_section_definition_id"/>
    <field labelOnTop="0" name="cross_section_definition_shape"/>
    <field labelOnTop="0" name="cross_section_definition_width"/>
    <field labelOnTop="0" name="def_code"/>
    <field labelOnTop="0" name="def_height"/>
    <field labelOnTop="0" name="def_id"/>
    <field labelOnTop="0" name="def_shape"/>
    <field labelOnTop="0" name="def_width"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="location_bank_level"/>
    <field labelOnTop="0" name="location_channel_id"/>
    <field labelOnTop="0" name="location_code"/>
    <field labelOnTop="0" name="location_definition_id"/>
    <field labelOnTop="0" name="location_friction_type"/>
    <field labelOnTop="0" name="location_friction_value"/>
    <field labelOnTop="0" name="location_id"/>
    <field labelOnTop="0" name="location_reference_level"/>
    <field labelOnTop="0" name="reference_level"/>
    <field labelOnTop="0" name="v2_cross_section_definition_code"/>
    <field labelOnTop="0" name="v2_cross_section_definition_height"/>
    <field labelOnTop="0" name="v2_cross_section_definition_shape"/>
    <field labelOnTop="0" name="v2_cross_section_definition_width"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>location_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
