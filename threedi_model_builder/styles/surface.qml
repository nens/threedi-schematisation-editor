<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0" version="3.16.3-Hannover" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 symbollevels="0" type="singleSymbol" forceraster="0" enableorderby="0">
    <symbols>
      <symbol name="0" clip_to_extent="1" alpha="1" force_rhr="0" type="fill">
        <layer locked="0" pass="0" class="SimpleFill" enabled="1">
          <prop k="border_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="color" v="244,198,119,255"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="133,112,8,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0.26"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="style" v="solid"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" value="" type="QString"/>
              <Option name="properties"/>
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
    <field name="display_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="zoom_category" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3" value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4" value="4" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="5" value="5" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="nr_of_inhabitants" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="area" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="dry_weather_flow" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="function" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_parameters_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="code" index="2"/>
    <alias name="" field="display_name" index="3"/>
    <alias name="" field="zoom_category" index="4"/>
    <alias name="" field="nr_of_inhabitants" index="5"/>
    <alias name="" field="area" index="6"/>
    <alias name="" field="dry_weather_flow" index="7"/>
    <alias name="" field="function" index="8"/>
    <alias name="" field="surface_parameters_id" index="9"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="code" expression="'new'" applyOnUpdate="0"/>
    <default field="display_name" expression="'new'" applyOnUpdate="0"/>
    <default field="zoom_category" expression="-1" applyOnUpdate="0"/>
    <default field="nr_of_inhabitants" expression="" applyOnUpdate="0"/>
    <default field="area" expression="$area" applyOnUpdate="0"/>
    <default field="dry_weather_flow" expression="" applyOnUpdate="0"/>
    <default field="function" expression="" applyOnUpdate="0"/>
    <default field="surface_parameters_id" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="code" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="display_name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="zoom_category" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="nr_of_inhabitants" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="area" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="dry_weather_flow" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="function" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="surface_parameters_id" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="display_name" desc="" exp=""/>
    <constraint field="zoom_category" desc="" exp=""/>
    <constraint field="nr_of_inhabitants" desc="" exp=""/>
    <constraint field="area" desc="" exp=""/>
    <constraint field="dry_weather_flow" desc="" exp=""/>
    <constraint field="function" desc="" exp=""/>
    <constraint field="surface_parameters_id" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1"></editform>
  <editforminit/>
  <editforminitcodesource>0</editforminitcodesource>
  <editforminitfilepath></editforminitfilepath>
  <editforminitcode><![CDATA[# -*- coding: utf-8 -*-
"""
QGIS forms can have a Python function that is called when the form is
opened.

Use this function to add extra logic to your forms.

Enter the name of the function in the "Python Init function"
field.
An example follows:
"""
from qgis.PyQt.QtWidgets import QWidget

def my_form_open(dialog, layer, feature):
	geom = feature.geometry()
	control = dialog.findChild(QWidget, "MyLineEdit")
]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>tablayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Surface" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorContainer name="General" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="id" index="1" showLabel="1"/>
        <attributeEditorField name="display_name" index="3" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Characteristics" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorContainer name="Rain water" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
          <attributeEditorField name="surface_parameters_id" index="9" showLabel="1"/>
          <attributeEditorField name="area" index="6" showLabel="1"/>
        </attributeEditorContainer>
        <attributeEditorContainer name="Municipal water" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
          <attributeEditorField name="nr_of_inhabitants" index="5" showLabel="1"/>
          <attributeEditorField name="dry_weather_flow" index="7" showLabel="1"/>
        </attributeEditorContainer>
      </attributeEditorContainer>
      <attributeEditorContainer name="Visualization" visibilityExpression="" groupBox="1" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
        <attributeEditorField name="zoom_category" index="4" showLabel="1"/>
        <attributeEditorField name="function" index="8" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="area" editable="1"/>
    <field name="code" editable="1"/>
    <field name="display_name" editable="1"/>
    <field name="dry_weather_flow" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="function" editable="1"/>
    <field name="id" editable="1"/>
    <field name="nr_of_inhabitants" editable="1"/>
    <field name="surface_parameters_id" editable="1"/>
    <field name="zoom_category" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="area" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="display_name" labelOnTop="0"/>
    <field name="dry_weather_flow" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="function" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="nr_of_inhabitants" labelOnTop="0"/>
    <field name="surface_parameters_id" labelOnTop="0"/>
    <field name="zoom_category" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"display_name"</previewExpression>
  <layerGeometryType>2</layerGeometryType>
</qgis>
