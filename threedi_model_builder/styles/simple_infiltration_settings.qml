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
    <field name="infiltration_rate" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file" configurationFlags="None">
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
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="infiltration_rate" index="2"/>
    <alias name="" field="infiltration_rate_file" index="3"/>
    <alias name="" field="infiltration_surface_option" index="4"/>
    <alias name="" field="max_infiltration_capacity_file" index="5"/>
    <alias name="" field="display_name" index="6"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1,maximum(id)+1)" applyOnUpdate="1"/>
    <default field="infiltration_rate" expression="" applyOnUpdate="0"/>
    <default field="infiltration_rate_file" expression="" applyOnUpdate="0"/>
    <default field="infiltration_surface_option" expression="0" applyOnUpdate="0"/>
    <default field="max_infiltration_capacity_file" expression="" applyOnUpdate="0"/>
    <default field="display_name" expression="'new'" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="infiltration_rate" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="infiltration_rate_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="infiltration_surface_option" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="max_infiltration_capacity_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="display_name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="infiltration_rate" desc="" exp=""/>
    <constraint field="infiltration_rate_file" desc="" exp=""/>
    <constraint field="infiltration_surface_option" desc="" exp=""/>
    <constraint field="max_infiltration_capacity_file" desc="" exp=""/>
    <constraint field="display_name" desc="" exp=""/>
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
      <attributeEditorField name="display_name" index="6" showLabel="1"/>
      <attributeEditorField name="infiltration_rate" index="2" showLabel="1"/>
      <attributeEditorField name="infiltration_rate_file" index="3" showLabel="1"/>
      <attributeEditorField name="max_infiltration_capacity_file" index="5" showLabel="1"/>
      <attributeEditorField name="infiltration_surface_option" index="4" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="display_name" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="infiltration_rate" editable="1"/>
    <field name="infiltration_rate_file" editable="1"/>
    <field name="infiltration_surface_option" editable="1"/>
    <field name="max_infiltration_capacity_file" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="display_name" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="infiltration_rate" labelOnTop="0"/>
    <field name="infiltration_rate_file" labelOnTop="0"/>
    <field name="infiltration_surface_option" labelOnTop="0"/>
    <field name="max_infiltration_capacity_file" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
