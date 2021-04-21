<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis simplifyAlgorithm="0" simplifyLocal="1" styleCategories="AllStyleCategories" labelsEnabled="0" version="3.16.4-Hannover" simplifyMaxScale="1" readOnly="0" maxScale="0" minScale="100000000" simplifyDrawingHints="0" simplifyDrawingTol="1" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal durationField="" durationUnit="min" startField="" mode="0" endField="" startExpression="" enabled="0" endExpression="" accumulate="0" fixedDuration="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <renderer-v2 enableorderby="0" forceraster="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol clip_to_extent="1" force_rhr="0" type="marker" name="0" alpha="1">
        <layer locked="0" pass="0" enabled="1" class="SimpleMarker">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="diamond"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option type="QString" name="name" value=""/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option type="bool" name="active" value="true"/>
                  <Option type="QString" name="expression" value="if(@map_scale&lt;10000, 2,0.5)"/>
                  <Option type="int" name="type" value="3"/>
                </Option>
              </Option>
              <Option type="QString" name="type" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <customproperties>
    <property key="dualview/previewExpressions" value="id"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerOpacity>1</layerOpacity>
  <SingleCategoryDiagramRenderer attributeLegend="1" diagramType="Histogram">
    <DiagramCategory spacingUnit="MM" maxScaleDenominator="1e+08" lineSizeType="MM" spacing="0" scaleDependency="Area" showAxis="0" scaleBasedVisibility="0" height="15" rotationOffset="270" direction="1" enabled="0" width="15" backgroundColor="#ffffff" minimumSize="0" penColor="#000000" sizeScale="3x:0,0,0,0,0,0" spacingUnitScale="3x:0,0,0,0,0,0" minScaleDenominator="0" labelPlacementMethod="XHeight" barWidth="5" sizeType="MM" lineSizeScale="3x:0,0,0,0,0,0" opacity="1" penWidth="0" diagramOrientation="Up" backgroundAlpha="255" penAlpha="255">
      <fontProperties description="MS Shell Dlg 2,8.25,-1,5,50,0,0,0,0,0" style=""/>
      <attribute field="" label="" color="#000000"/>
      <axisSymbol>
        <symbol clip_to_extent="1" force_rhr="0" type="line" name="" alpha="1">
          <layer locked="0" pass="0" enabled="1" class="SimpleLine">
            <prop k="align_dash_pattern" v="0"/>
            <prop k="capstyle" v="square"/>
            <prop k="customdash" v="5;2"/>
            <prop k="customdash_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="customdash_unit" v="MM"/>
            <prop k="dash_pattern_offset" v="0"/>
            <prop k="dash_pattern_offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="dash_pattern_offset_unit" v="MM"/>
            <prop k="draw_inside_polygon" v="0"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="line_color" v="35,35,35,255"/>
            <prop k="line_style" v="solid"/>
            <prop k="line_width" v="0.26"/>
            <prop k="line_width_unit" v="MM"/>
            <prop k="offset" v="0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="ring_filter" v="0"/>
            <prop k="tweak_dash_pattern_on_corners" v="0"/>
            <prop k="use_custom_dash" v="0"/>
            <prop k="width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" name="name" value=""/>
                <Option name="properties"/>
                <Option type="QString" name="type" value="collection"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </axisSymbol>
    </DiagramCategory>
  </SingleCategoryDiagramRenderer>
  <DiagramLayerSettings obstacle="0" linePlacementFlags="18" placement="0" dist="0" showAll="1" zIndex="0" priority="0">
    <properties>
      <Option type="Map">
        <Option type="QString" name="name" value=""/>
        <Option name="properties"/>
        <Option type="QString" name="type" value="collection"/>
      </Option>
    </properties>
  </DiagramLayerSettings>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend type="default-vector"/>
  <referencedLayers/>
  <fieldConfiguration>
    <field configurationFlags="None" name="ROWID">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_reference_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_bank_level">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: Chèzy" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: Manning" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_friction_value">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_definition_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="loc_channel_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="def_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="def_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="1: rectangle" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="2: round" value="2"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="3: egg" value="3"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="5: tabulated rectangle" value="5"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="6: tabulated trapezium" value="6"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="def_width">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="def_code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="def_height">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="ROWID" name="" index="0"/>
    <alias field="loc_id" name="id" index="1"/>
    <alias field="loc_code" name="code" index="2"/>
    <alias field="loc_reference_level" name="reference_level" index="3"/>
    <alias field="loc_bank_level" name="bank_level" index="4"/>
    <alias field="loc_friction_type" name="friction_type" index="5"/>
    <alias field="loc_friction_value" name="friction_value" index="6"/>
    <alias field="loc_definition_id" name="definition_id" index="7"/>
    <alias field="loc_channel_id" name="channel_id" index="8"/>
    <alias field="def_id" name="" index="9"/>
    <alias field="def_shape" name="" index="10"/>
    <alias field="def_width" name="" index="11"/>
    <alias field="def_code" name="" index="12"/>
    <alias field="def_height" name="" index="13"/>
  </aliases>
  <defaults>
    <default field="ROWID" applyOnUpdate="0" expression=""/>
    <default field="loc_id" applyOnUpdate="0" expression="if(maximum(loc_id) is null,1,maximum(loc_id)+1)"/>
    <default field="loc_code" applyOnUpdate="0" expression="'new'"/>
    <default field="loc_reference_level" applyOnUpdate="0" expression=""/>
    <default field="loc_bank_level" applyOnUpdate="0" expression=""/>
    <default field="loc_friction_type" applyOnUpdate="0" expression="2"/>
    <default field="loc_friction_value" applyOnUpdate="0" expression=""/>
    <default field="loc_definition_id" applyOnUpdate="0" expression=""/>
    <default field="loc_channel_id" applyOnUpdate="0" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))"/>
    <default field="def_id" applyOnUpdate="0" expression=""/>
    <default field="def_shape" applyOnUpdate="0" expression=""/>
    <default field="def_width" applyOnUpdate="0" expression=""/>
    <default field="def_code" applyOnUpdate="0" expression=""/>
    <default field="def_height" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="ROWID" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="loc_id" constraints="1" unique_strength="0" notnull_strength="2"/>
    <constraint exp_strength="0" field="loc_code" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="loc_reference_level" constraints="1" unique_strength="0" notnull_strength="2"/>
    <constraint exp_strength="0" field="loc_bank_level" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="loc_friction_type" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="loc_friction_value" constraints="1" unique_strength="0" notnull_strength="2"/>
    <constraint exp_strength="0" field="loc_definition_id" constraints="1" unique_strength="0" notnull_strength="2"/>
    <constraint exp_strength="0" field="loc_channel_id" constraints="1" unique_strength="0" notnull_strength="2"/>
    <constraint exp_strength="0" field="def_id" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="def_shape" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="def_width" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="def_code" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="def_height" constraints="0" unique_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="ROWID" desc=""/>
    <constraint exp="" field="loc_id" desc=""/>
    <constraint exp="" field="loc_code" desc=""/>
    <constraint exp="" field="loc_reference_level" desc=""/>
    <constraint exp="" field="loc_bank_level" desc=""/>
    <constraint exp="" field="loc_friction_type" desc=""/>
    <constraint exp="" field="loc_friction_value" desc=""/>
    <constraint exp="" field="loc_definition_id" desc=""/>
    <constraint exp="" field="loc_channel_id" desc=""/>
    <constraint exp="" field="def_id" desc=""/>
    <constraint exp="" field="def_shape" desc=""/>
    <constraint exp="" field="def_width" desc=""/>
    <constraint exp="" field="def_code" desc=""/>
    <constraint exp="" field="def_height" desc=""/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" actionWidgetStyle="dropDown" sortExpression="">
    <columns>
      <column width="-1" type="actions" hidden="1"/>
      <column width="-1" type="field" name="def_id" hidden="0"/>
      <column width="-1" type="field" name="def_shape" hidden="0"/>
      <column width="-1" type="field" name="def_width" hidden="0"/>
      <column width="-1" type="field" name="def_code" hidden="0"/>
      <column width="-1" type="field" name="def_height" hidden="0"/>
      <column width="-1" type="field" name="ROWID" hidden="0"/>
      <column width="-1" type="field" name="loc_id" hidden="0"/>
      <column width="-1" type="field" name="loc_code" hidden="0"/>
      <column width="-1" type="field" name="loc_reference_level" hidden="0"/>
      <column width="-1" type="field" name="loc_bank_level" hidden="0"/>
      <column width="-1" type="field" name="loc_friction_type" hidden="0"/>
      <column width="-1" type="field" name="loc_friction_value" hidden="0"/>
      <column width="-1" type="field" name="loc_definition_id" hidden="0"/>
      <column width="-1" type="field" name="loc_channel_id" hidden="0"/>
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
    <attributeEditorContainer columnCount="1" visibilityExpression="" showLabel="1" groupBox="0" visibilityExpressionEnabled="0" name="Cross section location view">
      <attributeEditorContainer columnCount="1" visibilityExpression="" showLabel="1" groupBox="1" visibilityExpressionEnabled="0" name="General">
        <attributeEditorField showLabel="1" name="loc_id" index="1"/>
        <attributeEditorField showLabel="1" name="loc_code" index="2"/>
        <attributeEditorField showLabel="1" name="loc_reference_level" index="3"/>
        <attributeEditorField showLabel="1" name="loc_bank_level" index="4"/>
        <attributeEditorField showLabel="1" name="loc_friction_type" index="5"/>
        <attributeEditorField showLabel="1" name="loc_friction_value" index="6"/>
        <attributeEditorField showLabel="1" name="loc_channel_id" index="8"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" visibilityExpression="" showLabel="1" groupBox="1" visibilityExpressionEnabled="0" name="Cross section">
        <attributeEditorField showLabel="1" name="loc_definition_id" index="7"/>
        <attributeEditorField showLabel="1" name="def_code" index="12"/>
        <attributeEditorField showLabel="1" name="def_shape" index="10"/>
        <attributeEditorField showLabel="1" name="def_width" index="11"/>
        <attributeEditorField showLabel="1" name="def_height" index="13"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="0" name="def_code"/>
    <field editable="0" name="def_height"/>
    <field editable="1" name="def_id"/>
    <field editable="0" name="def_shape"/>
    <field editable="0" name="def_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="loc_bank_level"/>
    <field editable="1" name="loc_channel_id"/>
    <field editable="1" name="loc_code"/>
    <field editable="1" name="loc_definition_id"/>
    <field editable="1" name="loc_friction_type"/>
    <field editable="1" name="loc_friction_value"/>
    <field editable="1" name="loc_id"/>
    <field editable="1" name="loc_reference_level"/>
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
    <field name="ROWID" labelOnTop="0"/>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="loc_bank_level" labelOnTop="0"/>
    <field name="loc_channel_id" labelOnTop="0"/>
    <field name="loc_code" labelOnTop="0"/>
    <field name="loc_definition_id" labelOnTop="0"/>
    <field name="loc_friction_type" labelOnTop="0"/>
    <field name="loc_friction_value" labelOnTop="0"/>
    <field name="loc_id" labelOnTop="0"/>
    <field name="loc_reference_level" labelOnTop="0"/>
    <field name="location_bank_level" labelOnTop="0"/>
    <field name="location_channel_id" labelOnTop="0"/>
    <field name="location_code" labelOnTop="0"/>
    <field name="location_definition_id" labelOnTop="0"/>
    <field name="location_friction_type" labelOnTop="0"/>
    <field name="location_friction_value" labelOnTop="0"/>
    <field name="location_id" labelOnTop="0"/>
    <field name="location_reference_level" labelOnTop="0"/>
    <field name="reference_level" labelOnTop="0"/>
    <field name="v2_cross_section_definition_code" labelOnTop="0"/>
    <field name="v2_cross_section_definition_height" labelOnTop="0"/>
    <field name="v2_cross_section_definition_shape" labelOnTop="0"/>
    <field name="v2_cross_section_definition_width" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>location_id</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>0</layerGeometryType>
</qgis>
