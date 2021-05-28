<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0" version="3.16.3-Hannover" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" force_rhr="0" type="marker">
        <layer locked="0" pass="0" class="SimpleMarker" enabled="1">
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
              <Option name="name" value="" type="QString"/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option name="active" value="true" type="bool"/>
                  <Option name="expression" value="if(@map_scale&lt;10000, 2,0.5)" type="QString"/>
                  <Option name="type" value="3" type="int"/>
                </Option>
              </Option>
              <Option name="type" value="collection" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reference_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
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
                <Option name="1: Chèzy" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" value="2" type="QString"/>
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
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_width" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_height" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_definition_shape" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" value="true" type="bool"/>
            <Option name="Max" value="2147483647" type="int"/>
            <Option name="Min" value="-2147483648" type="int"/>
            <Option name="Precision" value="0" type="int"/>
            <Option name="Step" value="1" type="int"/>
            <Option name="Style" value="SpinBox" type="QString"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="id" field="id" index="1"/>
    <alias name="code" field="code" index="2"/>
    <alias name="reference_level" field="reference_level" index="3"/>
    <alias name="friction_type" field="friction_type" index="4"/>
    <alias name="friction_value" field="friction_value" index="5"/>
    <alias name="bank_level" field="bank_level" index="6"/>
    <alias name="channel_id" field="channel_id" index="7"/>
    <alias name="" field="cross_section_definition_id" index="8"/>
    <alias name="" field="cross_section_definition_code" index="9"/>
    <alias name="" field="cross_section_definition_width" index="10"/>
    <alias name="" field="cross_section_definition_height" index="11"/>
    <alias name="" field="cross_section_definition_shape" index="12"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1,maximum(id)+1)" applyOnUpdate="1"/>
    <default field="code" expression="'new'" applyOnUpdate="0"/>
    <default field="reference_level" expression="" applyOnUpdate="0"/>
    <default field="friction_type" expression="2" applyOnUpdate="0"/>
    <default field="friction_value" expression="" applyOnUpdate="0"/>
    <default field="bank_level" expression="" applyOnUpdate="0"/>
    <default field="channel_id" expression="aggregate('v2_channel','min',&quot;id&quot;, intersects($geometry,geometry(@parent)))" applyOnUpdate="0"/>
    <default field="cross_section_definition_id" expression="" applyOnUpdate="0"/>
    <default field="cross_section_definition_code" expression="'new'" applyOnUpdate="0"/>
    <default field="cross_section_definition_width" expression="" applyOnUpdate="0"/>
    <default field="cross_section_definition_height" expression="" applyOnUpdate="0"/>
    <default field="cross_section_definition_shape" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="code" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="reference_level" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="friction_type" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="friction_value" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="bank_level" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="channel_id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="cross_section_definition_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="cross_section_definition_code" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="cross_section_definition_width" constraints="5" exp_strength="2" notnull_strength="2" unique_strength="0"/>
    <constraint field="cross_section_definition_height" constraints="4" exp_strength="2" notnull_strength="0" unique_strength="0"/>
    <constraint field="cross_section_definition_shape" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="reference_level" desc="" exp=""/>
    <constraint field="friction_type" desc="" exp=""/>
    <constraint field="friction_value" desc="" exp=""/>
    <constraint field="bank_level" desc="" exp=""/>
    <constraint field="channel_id" desc="" exp=""/>
    <constraint field="cross_section_definition_id" desc="" exp=""/>
    <constraint field="cross_section_definition_code" desc="" exp=""/>
    <constraint field="cross_section_definition_width" desc="" exp="regexp_match(&quot;width&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$')"/>
    <constraint field="cross_section_definition_height" desc="" exp="regexp_match(&quot;height&quot;,'^(-?\\d+(\\.\\d+)?)(\\s-?\\d+(\\.\\d+)?)*$') or &quot;height&quot;is null"/>
    <constraint field="cross_section_definition_shape" desc="" exp=""/>
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
    <attributeEditorContainer name="Cross section location view" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorContainer name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="id" index="1" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
        <attributeEditorField name="reference_level" index="3" showLabel="1"/>
        <attributeEditorField name="bank_level" index="6" showLabel="1"/>
        <attributeEditorField name="friction_type" index="4" showLabel="1"/>
        <attributeEditorField name="friction_value" index="5" showLabel="1"/>
        <attributeEditorField name="channel_id" index="7" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="cross_section_definition_id" index="8" showLabel="1"/>
        <attributeEditorField name="cross_section_definition_shape" index="12" showLabel="1"/>
        <attributeEditorField name="cross_section_definition_height" index="11" showLabel="1"/>
        <attributeEditorField name="cross_section_definition_width" index="10" showLabel="1"/>
        <attributeEditorField name="cross_section_definition_code" index="9" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="Cross section definition_code" editable="0"/>
    <field name="Cross section definition_height" editable="0"/>
    <field name="Cross section definition_shape" editable="0"/>
    <field name="Cross section definition_width" editable="0"/>
    <field name="ROWID" editable="1"/>
    <field name="bank_level" editable="1"/>
    <field name="channel_id" editable="1"/>
    <field name="code" editable="1"/>
    <field name="cross_section_definition_code" editable="0"/>
    <field name="cross_section_definition_height" editable="0"/>
    <field name="cross_section_definition_id" editable="1"/>
    <field name="cross_section_definition_shape" editable="0"/>
    <field name="cross_section_definition_width" editable="0"/>
    <field name="def_code" editable="0"/>
    <field name="def_height" editable="0"/>
    <field name="def_id" editable="1"/>
    <field name="def_shape" editable="0"/>
    <field name="def_width" editable="0"/>
    <field name="definition_id" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="friction_type" editable="1"/>
    <field name="friction_value" editable="1"/>
    <field name="id" editable="1"/>
    <field name="location_bank_level" editable="1"/>
    <field name="location_channel_id" editable="1"/>
    <field name="location_code" editable="1"/>
    <field name="location_definition_id" editable="1"/>
    <field name="location_friction_type" editable="1"/>
    <field name="location_friction_value" editable="1"/>
    <field name="location_id" editable="1"/>
    <field name="location_reference_level" editable="1"/>
    <field name="reference_level" editable="1"/>
    <field name="v2_cross_section_definition_code" editable="0"/>
    <field name="v2_cross_section_definition_height" editable="0"/>
    <field name="v2_cross_section_definition_shape" editable="0"/>
    <field name="v2_cross_section_definition_width" editable="0"/>
  </editable>
  <labelOnTop>
    <field name="Cross section definition_code" labelOnTop="0"/>
    <field name="Cross section definition_height" labelOnTop="0"/>
    <field name="Cross section definition_shape" labelOnTop="0"/>
    <field name="Cross section definition_width" labelOnTop="0"/>
    <field name="ROWID" labelOnTop="0"/>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="cross_section_definition_code" labelOnTop="0"/>
    <field name="cross_section_definition_height" labelOnTop="0"/>
    <field name="cross_section_definition_id" labelOnTop="0"/>
    <field name="cross_section_definition_shape" labelOnTop="0"/>
    <field name="cross_section_definition_width" labelOnTop="0"/>
    <field name="def_code" labelOnTop="0"/>
    <field name="def_height" labelOnTop="0"/>
    <field name="def_id" labelOnTop="0"/>
    <field name="def_shape" labelOnTop="0"/>
    <field name="def_width" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
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
  <layerGeometryType>0</layerGeometryType>
</qgis>
