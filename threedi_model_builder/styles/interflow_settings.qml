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
    <field name="interflow_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="0: No interflow" value="0" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="1: Porosity is rescaled per computational cell with respect to the deepest surface level in that cell. (Defining the porosity_layer_thickness is mandatory)" value="1" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="2: Porosity is rescaled per computational cell with respect to the deepest surface level in the 2D surface domain. (Defining the porosity_layer_thickness is mandatory)" value="2" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="3: The impervious layer thickness is uniform in the 2D surface domain and is based on the impervious_layer_elevation and the deepest surface level in that cell." value="3" type="QString"/>
              </Option>
              <Option type="Map">
                <Option name="4: The impervious layer thickness is non-uniform in the 2D surface domain and is based on the impervious_layer_elevation with respect to the deepest surface level in the 2D surface domain." value="4" type="QString"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="porosity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="porosity_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="porosity_layer_thickness" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="impervious_layer_elevation" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hydraulic_conductivity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="hydraulic_conductivity_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
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
    <alias name="" field="interflow_type" index="2"/>
    <alias name="" field="porosity" index="3"/>
    <alias name="" field="porosity_file" index="4"/>
    <alias name="" field="porosity_layer_thickness" index="5"/>
    <alias name="" field="impervious_layer_elevation" index="6"/>
    <alias name="" field="hydraulic_conductivity" index="7"/>
    <alias name="" field="hydraulic_conductivity_file" index="8"/>
    <alias name="" field="display_name" index="9"/>
  </aliases>
  <defaults>
    <default field="fid" expression="" applyOnUpdate="0"/>
    <default field="id" expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="1"/>
    <default field="interflow_type" expression="" applyOnUpdate="0"/>
    <default field="porosity" expression="" applyOnUpdate="0"/>
    <default field="porosity_file" expression="" applyOnUpdate="0"/>
    <default field="porosity_layer_thickness" expression="" applyOnUpdate="0"/>
    <default field="impervious_layer_elevation" expression="" applyOnUpdate="0"/>
    <default field="hydraulic_conductivity" expression="" applyOnUpdate="0"/>
    <default field="hydraulic_conductivity_file" expression="" applyOnUpdate="0"/>
    <default field="display_name" expression="" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint field="fid" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="id" constraints="3" exp_strength="0" notnull_strength="1" unique_strength="1"/>
    <constraint field="interflow_type" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
    <constraint field="porosity" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="porosity_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="porosity_layer_thickness" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="impervious_layer_elevation" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="hydraulic_conductivity" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="hydraulic_conductivity_file" constraints="0" exp_strength="0" notnull_strength="0" unique_strength="0"/>
    <constraint field="display_name" constraints="1" exp_strength="0" notnull_strength="2" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="interflow_type" desc="" exp=""/>
    <constraint field="porosity" desc="" exp=""/>
    <constraint field="porosity_file" desc="" exp=""/>
    <constraint field="porosity_layer_thickness" desc="" exp=""/>
    <constraint field="impervious_layer_elevation" desc="" exp=""/>
    <constraint field="hydraulic_conductivity" desc="" exp=""/>
    <constraint field="hydraulic_conductivity_file" desc="" exp=""/>
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
      <attributeEditorField name="display_name" index="9" showLabel="1"/>
      <attributeEditorField name="interflow_type" index="2" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Porosity" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="porosity" index="3" showLabel="1"/>
      <attributeEditorField name="porosity_file" index="4" showLabel="1"/>
      <attributeEditorField name="porosity_layer_thickness" index="5" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Hydraulic conductivity" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="hydraulic_conductivity_file" index="8" showLabel="1"/>
      <attributeEditorField name="hydraulic_conductivity" index="7" showLabel="1"/>
    </attributeEditorContainer>
    <attributeEditorContainer name="Impervious layer" visibilityExpression="" groupBox="0" visibilityExpressionEnabled="0" columnCount="1" showLabel="1">
      <attributeEditorField name="impervious_layer_elevation" index="6" showLabel="1"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="display_name" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="hydraulic_conductivity" editable="1"/>
    <field name="hydraulic_conductivity_file" editable="1"/>
    <field name="id" editable="1"/>
    <field name="impervious_layer_elevation" editable="1"/>
    <field name="interflow_type" editable="1"/>
    <field name="porosity" editable="1"/>
    <field name="porosity_file" editable="1"/>
    <field name="porosity_layer_thickness" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="display_name" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="hydraulic_conductivity" labelOnTop="0"/>
    <field name="hydraulic_conductivity_file" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="impervious_layer_elevation" labelOnTop="0"/>
    <field name="interflow_type" labelOnTop="0"/>
    <field name="porosity" labelOnTop="0"/>
    <field name="porosity_file" labelOnTop="0"/>
    <field name="porosity_layer_thickness" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>4</layerGeometryType>
</qgis>
