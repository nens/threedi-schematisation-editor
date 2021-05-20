<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.3-Hannover" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" symbollevels="0" enableorderby="0" type="singleSymbol">
    <symbols>
      <symbol name="0" alpha="1" clip_to_extent="1" type="marker" force_rhr="0">
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
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
              <Option value="" name="name" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option value="true" name="active" type="bool"/>
                  <Option value="if(@map_scale&lt;10000, 2,0.5)" name="expression" type="QString"/>
                  <Option value="3" name="type" type="int"/>
                </Option>
              </Option>
              <Option value="collection" name="type" type="QString"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reference_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option value="1" name="1: Chèzy" type="QString"/>
              </Option>
              <Option type="Map">
                <Option value="2" name="2: Manning" type="QString"/>
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
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="2147483647" name="Max" type="int"/>
            <Option value="-2147483648" name="Min" type="int"/>
            <Option value="0" name="Precision" type="int"/>
            <Option value="1" name="Step" type="int"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" name="IsMultiline" type="bool"/>
            <Option value="false" name="UseHtml" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_shape" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" name="AllowNull" type="bool"/>
            <Option value="2147483647" name="Max" type="int"/>
            <Option value="-2147483648" name="Min" type="int"/>
            <Option value="0" name="Precision" type="int"/>
            <Option value="1" name="Step" type="int"/>
            <Option value="SpinBox" name="Style" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias index="0" field="fid" name=""/>
    <alias index="1" field="id" name="id"/>
    <alias index="2" field="code" name="code"/>
    <alias index="3" field="reference_level" name="reference_level"/>
    <alias index="4" field="friction_type" name="friction_type"/>
    <alias index="5" field="friction_value" name="friction_value"/>
    <alias index="6" field="bank_level" name="bank_level"/>
    <alias index="7" field="channel_id" name="channel_id"/>
    <alias index="8" field="cross_section_definition_id" name=""/>
    <alias index="9" field="cross_section_definition_code" name=""/>
    <alias index="10" field="cross_section_definition_width" name=""/>
    <alias index="11" field="cross_section_definition_height" name=""/>
    <alias index="12" field="cross_section_definition_shape" name=""/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" field="fid" expression=""/>
    <default applyOnUpdate="0" field="id" expression="if(maximum(id) is null,1,maximum(id)+1)"/>
    <default applyOnUpdate="0" field="code" expression="'new'"/>
    <default applyOnUpdate="0" field="reference_level" expression=""/>
    <default applyOnUpdate="0" field="friction_type" expression="2"/>
    <default applyOnUpdate="0" field="friction_value" expression=""/>
    <default applyOnUpdate="0" field="bank_level" expression=""/>
    <default applyOnUpdate="0" field="channel_id" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))"/>
    <default applyOnUpdate="0" field="cross_section_definition_id" expression=""/>
    <default applyOnUpdate="0" field="cross_section_definition_code" expression="'new'"/>
    <default applyOnUpdate="0" field="cross_section_definition_width" expression=""/>
    <default applyOnUpdate="0" field="cross_section_definition_height" expression=""/>
    <default applyOnUpdate="0" field="cross_section_definition_shape" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" field="fid" constraints="3" exp_strength="0" notnull_strength="1"/>
    <constraint unique_strength="0" field="id" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="code" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="reference_level" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="friction_type" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="friction_value" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="bank_level" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="channel_id" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="cross_section_definition_id" constraints="0" exp_strength="0" notnull_strength="0"/>
    <constraint unique_strength="0" field="cross_section_definition_code" constraints="1" exp_strength="0" notnull_strength="2"/>
    <constraint unique_strength="0" field="cross_section_definition_width" constraints="5" exp_strength="2" notnull_strength="2"/>
    <constraint unique_strength="0" field="cross_section_definition_height" constraints="4" exp_strength="2" notnull_strength="0"/>
    <constraint unique_strength="0" field="cross_section_definition_shape" constraints="1" exp_strength="0" notnull_strength="2"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" field="fid" desc=""/>
    <constraint exp="" field="id" desc=""/>
    <constraint exp="" field="code" desc=""/>
    <constraint exp="" field="reference_level" desc=""/>
    <constraint exp="" field="friction_type" desc=""/>
    <constraint exp="" field="friction_value" desc=""/>
    <constraint exp="" field="bank_level" desc=""/>
    <constraint exp="" field="channel_id" desc=""/>
    <constraint exp="" field="cross_section_definition_id" desc=""/>
    <constraint exp="" field="cross_section_definition_code" desc=""/>
    <constraint exp="regexp_match(&quot;width&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$')" field="cross_section_definition_width" desc=""/>
    <constraint exp="regexp_match(&quot;height&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$') or &quot;height&quot;is null" field="cross_section_definition_height" desc=""/>
    <constraint exp="" field="cross_section_definition_shape" desc=""/>
  </constraintExpressions>
  <expressionfields/>
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
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" name="Cross section location view" columnCount="1" visibilityExpressionEnabled="0">
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" name="General" columnCount="1" visibilityExpressionEnabled="0">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="reference_level"/>
        <attributeEditorField showLabel="1" index="6" name="bank_level"/>
        <attributeEditorField showLabel="1" index="4" name="friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="friction_value"/>
        <attributeEditorField showLabel="1" index="7" name="channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpression="" name="Cross section" columnCount="1" visibilityExpressionEnabled="0">
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
