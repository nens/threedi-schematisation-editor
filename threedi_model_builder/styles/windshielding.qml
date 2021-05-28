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
    <field name="north" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="northeast" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="east" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="southeast" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" value="false" type="bool"/>
            <Option name="UseHtml" value="false" type="bool"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="south" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="southwest" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="west" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="northwest" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
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
  </fieldConfiguration>
  <aliases>
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="north" index="2"/>
    <alias name="" field="northeast" index="3"/>
    <alias name="" field="east" index="4"/>
    <alias name="" field="southeast" index="5"/>
    <alias name="" field="south" index="6"/>
    <alias name="" field="southwest" index="7"/>
    <alias name="" field="west" index="8"/>
    <alias name="" field="northwest" index="9"/>
    <alias name="" field="channel_id" index="10"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="north" expression="" applyOnUpdate="0"/>
    <default field="northeast" expression="" applyOnUpdate="0"/>
    <default field="east" expression="" applyOnUpdate="0"/>
    <default field="southeast" expression="" applyOnUpdate="0"/>
    <default field="south" expression="" applyOnUpdate="0"/>
    <default field="southwest" expression="" applyOnUpdate="0"/>
    <default field="west" expression="" applyOnUpdate="0"/>
    <default field="northwest" expression="" applyOnUpdate="0"/>
    <default field="channel_id" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="north" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="northeast" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="east" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="southeast" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="south" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="southwest" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="west" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="northwest" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="channel_id" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="north" desc="" exp=""/>
    <constraint field="northeast" desc="" exp=""/>
    <constraint field="east" desc="" exp=""/>
    <constraint field="southeast" desc="" exp=""/>
    <constraint field="south" desc="" exp=""/>
    <constraint field="southwest" desc="" exp=""/>
    <constraint field="west" desc="" exp=""/>
    <constraint field="northwest" desc="" exp=""/>
    <constraint field="channel_id" desc="" exp=""/>
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
      <attributeEditorField name="channel_id" index="10" showLabel="1"/>
      <attributeEditorField name="north" index="2" showLabel="1"/>
      <attributeEditorField name="northeast" index="3" showLabel="1"/>
      <attributeEditorField name="east" index="4" showLabel="1"/>
      <attributeEditorField name="southeast" index="5" showLabel="1"/>
      <attributeEditorField name="south" index="6" showLabel="1"/>
      <attributeEditorField name="southwest" index="7" showLabel="1"/>
      <attributeEditorField name="west" index="8" showLabel="1"/>
      <attributeEditorField name="northwest" index="9" showLabel="1"/>
      <attributeEditorField name="the_geom" index="-1" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="channel_id" editable="1"/>
    <field name="east" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="id" editable="1"/>
    <field name="north" editable="1"/>
    <field name="northeast" editable="1"/>
    <field name="northwest" editable="1"/>
    <field name="south" editable="1"/>
    <field name="southeast" editable="1"/>
    <field name="southwest" editable="1"/>
    <field name="the_geom" editable="1"/>
    <field name="west" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="channel_id" labelOnTop="0"/>
    <field name="east" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="north" labelOnTop="0"/>
    <field name="northeast" labelOnTop="0"/>
    <field name="northwest" labelOnTop="0"/>
    <field name="south" labelOnTop="0"/>
    <field name="southeast" labelOnTop="0"/>
    <field name="southwest" labelOnTop="0"/>
    <field name="the_geom" labelOnTop="0"/>
    <field name="west" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
