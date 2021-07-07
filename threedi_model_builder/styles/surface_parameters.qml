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
    <field name="outflow_delay" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="surface_layer_thickness" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="min_infiltration_capacity" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_decay_constant" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_recovery_constant" configurationFlags="None">
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
    <alias field="outflow_delay" index="2" name=""/>
    <alias field="surface_layer_thickness" index="3" name=""/>
    <alias field="infiltration" index="4" name=""/>
    <alias field="max_infiltration_capacity" index="5" name=""/>
    <alias field="min_infiltration_capacity" index="6" name=""/>
    <alias field="infiltration_decay_constant" index="7" name=""/>
    <alias field="infiltration_recovery_constant" index="8" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="outflow_delay"/>
    <default expression="" applyOnUpdate="0" field="surface_layer_thickness"/>
    <default expression="" applyOnUpdate="0" field="infiltration"/>
    <default expression="" applyOnUpdate="0" field="max_infiltration_capacity"/>
    <default expression="" applyOnUpdate="0" field="min_infiltration_capacity"/>
    <default expression="" applyOnUpdate="0" field="infiltration_decay_constant"/>
    <default expression="" applyOnUpdate="0" field="infiltration_recovery_constant"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="outflow_delay" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="surface_layer_thickness" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="infiltration" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="max_infiltration_capacity" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="min_infiltration_capacity" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="infiltration_decay_constant" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="infiltration_recovery_constant" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="outflow_delay"/>
    <constraint exp="" desc="" field="surface_layer_thickness"/>
    <constraint exp="" desc="" field="infiltration"/>
    <constraint exp="" desc="" field="max_infiltration_capacity"/>
    <constraint exp="" desc="" field="min_infiltration_capacity"/>
    <constraint exp="" desc="" field="infiltration_decay_constant"/>
    <constraint exp="" desc="" field="infiltration_recovery_constant"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="outflow_delay"/>
      <column width="-1" hidden="0" type="field" name="surface_layer_thickness"/>
      <column width="-1" hidden="0" type="field" name="infiltration"/>
      <column width="-1" hidden="0" type="field" name="max_infiltration_capacity"/>
      <column width="-1" hidden="0" type="field" name="min_infiltration_capacity"/>
      <column width="-1" hidden="0" type="field" name="infiltration_decay_constant"/>
      <column width="-1" hidden="0" type="field" name="infiltration_recovery_constant"/>
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
      <attributeEditorField showLabel="1" index="4" name="infiltration"/>
      <attributeEditorField showLabel="1" index="5" name="max_infiltration_capacity"/>
      <attributeEditorField showLabel="1" index="6" name="min_infiltration_capacity"/>
      <attributeEditorField showLabel="1" index="7" name="infiltration_decay_constant"/>
      <attributeEditorField showLabel="1" index="8" name="infiltration_recovery_constant"/>
      <attributeEditorField showLabel="1" index="3" name="surface_layer_thickness"/>
      <attributeEditorField showLabel="1" index="2" name="outflow_delay"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltration"/>
    <field editable="1" name="infiltration_decay_constant"/>
    <field editable="1" name="infiltration_recovery_constant"/>
    <field editable="1" name="max_infiltration_capacity"/>
    <field editable="1" name="min_infiltration_capacity"/>
    <field editable="1" name="outflow_delay"/>
    <field editable="1" name="surface_layer_thickness"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltration"/>
    <field labelOnTop="0" name="infiltration_decay_constant"/>
    <field labelOnTop="0" name="infiltration_recovery_constant"/>
    <field labelOnTop="0" name="max_infiltration_capacity"/>
    <field labelOnTop="0" name="min_infiltration_capacity"/>
    <field labelOnTop="0" name="outflow_delay"/>
    <field labelOnTop="0" name="surface_layer_thickness"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
