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
    <field name="outflow_delay" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_layer_thickness" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="min_infiltration_capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_decay_constant" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_recovery_constant" configurationFlags="None">
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
    <alias name="" field="outflow_delay" index="2"/>
    <alias name="" field="surface_layer_thickness" index="3"/>
    <alias name="" field="infiltration" index="4"/>
    <alias name="" field="max_infiltration_capacity" index="5"/>
    <alias name="" field="min_infiltration_capacity" index="6"/>
    <alias name="" field="infiltration_decay_constant" index="7"/>
    <alias name="" field="infiltration_recovery_constant" index="8"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="outflow_delay" expression="" applyOnUpdate="0"/>
    <default field="surface_layer_thickness" expression="" applyOnUpdate="0"/>
    <default field="infiltration" expression="" applyOnUpdate="0"/>
    <default field="max_infiltration_capacity" expression="" applyOnUpdate="0"/>
    <default field="min_infiltration_capacity" expression="" applyOnUpdate="0"/>
    <default field="infiltration_decay_constant" expression="" applyOnUpdate="0"/>
    <default field="infiltration_recovery_constant" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="outflow_delay" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="surface_layer_thickness" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="infiltration" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="max_infiltration_capacity" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="min_infiltration_capacity" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="infiltration_decay_constant" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="infiltration_recovery_constant" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="outflow_delay" desc="" exp=""/>
    <constraint field="surface_layer_thickness" desc="" exp=""/>
    <constraint field="infiltration" desc="" exp=""/>
    <constraint field="max_infiltration_capacity" desc="" exp=""/>
    <constraint field="min_infiltration_capacity" desc="" exp=""/>
    <constraint field="infiltration_decay_constant" desc="" exp=""/>
    <constraint field="infiltration_recovery_constant" desc="" exp=""/>
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
      <attributeEditorField name="infiltration" index="4" showLabel="1"/>
      <attributeEditorField name="max_infiltration_capacity" index="5" showLabel="1"/>
      <attributeEditorField name="min_infiltration_capacity" index="6" showLabel="1"/>
      <attributeEditorField name="infiltration_decay_constant" index="7" showLabel="1"/>
      <attributeEditorField name="infiltration_recovery_constant" index="8" showLabel="1"/>
      <attributeEditorField name="surface_layer_thickness" index="3" showLabel="1"/>
      <attributeEditorField name="outflow_delay" index="2" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="infiltration" editable="1"/>
    <field name="infiltration_decay_constant" editable="1"/>
    <field name="infiltration_recovery_constant" editable="1"/>
    <field name="max_infiltration_capacity" editable="1"/>
    <field name="min_infiltration_capacity" editable="1"/>
    <field name="outflow_delay" editable="1"/>
    <field name="surface_layer_thickness" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="infiltration" labelOnTop="0"/>
    <field name="infiltration_decay_constant" labelOnTop="0"/>
    <field name="infiltration_recovery_constant" labelOnTop="0"/>
    <field name="max_infiltration_capacity" labelOnTop="0"/>
    <field name="min_infiltration_capacity" labelOnTop="0"/>
    <field name="outflow_delay" labelOnTop="0"/>
    <field name="surface_layer_thickness" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
