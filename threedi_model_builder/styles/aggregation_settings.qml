<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" version="3.16.3-Hannover" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
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
    <field name="global_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="var_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flow_variable" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="discharge" value="discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="flow velocity" value="flow_velocity" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="pump discharge" value="pump_discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="rain" value="rain" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="waterlevel" value="waterlevel" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="wet cross section" value="wet_cross-section" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="wet surface" value="wet_surface" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="lateral discharge" value="lateral_discharge" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="volume" value="volume" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="infiltration" value="simple_infiltration" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="leakage" value="leakage" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="interception" value="interception" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_method" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="average" value="avg" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="minimum" value="min" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="maximum" value="max" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="cumulative" value="cum" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="median" value="med" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="cumulative negative" value="cum_negative" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="cumulative positive" value="cum_positive" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="current" value="current" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="aggregation_in_space" configurationFlags="None">
      <editWidget type="Hidden">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="timestep" configurationFlags="None">
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
    <alias name="" field="global_settings_id" index="2"/>
    <alias name="" field="var_name" index="3"/>
    <alias name="" field="flow_variable" index="4"/>
    <alias name="" field="aggregation_method" index="5"/>
    <alias name="" field="aggregation_in_space" index="6"/>
    <alias name="" field="timestep" index="7"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="global_settings_id" expression="" applyOnUpdate="0"/>
    <default field="var_name" expression="" applyOnUpdate="0"/>
    <default field="flow_variable" expression="" applyOnUpdate="0"/>
    <default field="aggregation_method" expression="" applyOnUpdate="0"/>
    <default field="aggregation_in_space" expression="0" applyOnUpdate="0"/>
    <default field="timestep" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="global_settings_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="var_name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="flow_variable" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="aggregation_method" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="aggregation_in_space" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="timestep" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="global_settings_id" desc="" exp=""/>
    <constraint field="var_name" desc="" exp=""/>
    <constraint field="flow_variable" desc="" exp=""/>
    <constraint field="aggregation_method" desc="" exp=""/>
    <constraint field="aggregation_in_space" desc="" exp=""/>
    <constraint field="timestep" desc="" exp=""/>
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
    <attributeEditorContainer name="General" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="id" index="1" showLabel="1"/>
      <attributeEditorField name="flow_variable" index="4" showLabel="1"/>
      <attributeEditorField name="aggregation_method" index="5" showLabel="1"/>
      <attributeEditorField name="timestep" index="7" showLabel="1"/>
      <attributeEditorField name="var_name" index="3" showLabel="1"/>
      <attributeEditorField name="global_settings_id" index="2" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="aggregation_in_space" editable="1"/>
    <field name="aggregation_method" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="flow_variable" editable="1"/>
    <field name="global_settings_id" editable="1"/>
    <field name="id" editable="1"/>
    <field name="timestep" editable="1"/>
    <field name="var_name" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="aggregation_in_space" labelOnTop="0"/>
    <field name="aggregation_method" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="flow_variable" labelOnTop="0"/>
    <field name="global_settings_id" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="timestep" labelOnTop="0"/>
    <field name="var_name" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"var_name"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
