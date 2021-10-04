<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis minScale="0" version="3.16.3-Hannover" readOnly="0" hasScaleBasedVisibilityFlag="0" maxScale="0" styleCategories="AllStyleCategories">
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
  <customproperties>
    <property value="0" key="embeddedWidgets/count"/>
    <property key="variableNames"/>
    <property key="variableValues"/>
  </customproperties>
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
    <field name="interflow_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: No interflow"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Porosity is rescaled per computational cell with respect to the deepest surface level in that cell. (Defining the porosity_layer_thickness is mandatory)"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Porosity is rescaled per computational cell with respect to the deepest surface level in the 2D surface domain. (Defining the porosity_layer_thickness is mandatory)"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: The impervious layer thickness is uniform in the 2D surface domain and is based on the impervious_layer_elevation and the deepest surface level in that cell."/>
              </Option>
              <Option type="Map">
                <Option value="4" type="QString" name="4: The impervious layer thickness is non-uniform in the 2D surface domain and is based on the impervious_layer_elevation with respect to the deepest surface level in the 2D surface domain."/>
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
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="interflow_type" index="2" name=""/>
    <alias field="porosity" index="3" name=""/>
    <alias field="porosity_file" index="4" name=""/>
    <alias field="porosity_layer_thickness" index="5" name=""/>
    <alias field="impervious_layer_elevation" index="6" name=""/>
    <alias field="hydraulic_conductivity" index="7" name=""/>
    <alias field="hydraulic_conductivity_file" index="8" name=""/>
    <alias field="display_name" index="9" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="interflow_type"/>
    <default expression="" applyOnUpdate="0" field="porosity"/>
    <default expression="" applyOnUpdate="0" field="porosity_file"/>
    <default expression="" applyOnUpdate="0" field="porosity_layer_thickness"/>
    <default expression="" applyOnUpdate="0" field="impervious_layer_elevation"/>
    <default expression="" applyOnUpdate="0" field="hydraulic_conductivity"/>
    <default expression="" applyOnUpdate="0" field="hydraulic_conductivity_file"/>
    <default expression="" applyOnUpdate="0" field="display_name"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="interflow_type" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="porosity" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="porosity_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="porosity_layer_thickness" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="impervious_layer_elevation" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="hydraulic_conductivity" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="hydraulic_conductivity_file" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="display_name" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="interflow_type"/>
    <constraint exp="" desc="" field="porosity"/>
    <constraint exp="" desc="" field="porosity_file"/>
    <constraint exp="" desc="" field="porosity_layer_thickness"/>
    <constraint exp="" desc="" field="impervious_layer_elevation"/>
    <constraint exp="" desc="" field="hydraulic_conductivity"/>
    <constraint exp="" desc="" field="hydraulic_conductivity_file"/>
    <constraint exp="" desc="" field="display_name"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="interflow_type"/>
      <column width="-1" hidden="0" type="field" name="porosity"/>
      <column width="-1" hidden="0" type="field" name="porosity_file"/>
      <column width="-1" hidden="0" type="field" name="porosity_layer_thickness"/>
      <column width="-1" hidden="0" type="field" name="impervious_layer_elevation"/>
      <column width="-1" hidden="0" type="field" name="hydraulic_conductivity"/>
      <column width="-1" hidden="0" type="field" name="hydraulic_conductivity_file"/>
      <column width="-1" hidden="0" type="field" name="display_name"/>
      <column width="-1" hidden="1" type="actions"/>
    </columns>
  </attributetableconfig>
  <conditionalstyles>
    <rowstyles/>
    <fieldstyles/>
  </conditionalstyles>
  <storedexpressions/>
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
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="General" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="1" name="id"/>
      <attributeEditorField showLabel="1" index="9" name="display_name"/>
      <attributeEditorField showLabel="1" index="2" name="interflow_type"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Porosity" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="3" name="porosity"/>
      <attributeEditorField showLabel="1" index="4" name="porosity_file"/>
      <attributeEditorField showLabel="1" index="5" name="porosity_layer_thickness"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Hydraulic conductivity" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="8" name="hydraulic_conductivity_file"/>
      <attributeEditorField showLabel="1" index="7" name="hydraulic_conductivity"/>
    </attributeEditorContainer>
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpression="" columnCount="1" name="Impervious layer" visibilityExpressionEnabled="0">
      <attributeEditorField showLabel="1" index="6" name="impervious_layer_elevation"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="display_name"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="hydraulic_conductivity"/>
    <field editable="1" name="hydraulic_conductivity_file"/>
    <field editable="1" name="id"/>
    <field editable="1" name="impervious_layer_elevation"/>
    <field editable="1" name="interflow_type"/>
    <field editable="1" name="porosity"/>
    <field editable="1" name="porosity_file"/>
    <field editable="1" name="porosity_layer_thickness"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="hydraulic_conductivity"/>
    <field labelOnTop="0" name="hydraulic_conductivity_file"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="impervious_layer_elevation"/>
    <field labelOnTop="0" name="interflow_type"/>
    <field labelOnTop="0" name="porosity"/>
    <field labelOnTop="0" name="porosity_file"/>
    <field labelOnTop="0" name="porosity_layer_thickness"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
