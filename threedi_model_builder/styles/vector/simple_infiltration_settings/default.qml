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
    <field name="infiltration_rate" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
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
    <alias field="infiltration_rate" index="2" name=""/>
    <alias field="infiltration_rate_file" index="3" name=""/>
    <alias field="infiltration_surface_option" index="4" name=""/>
    <alias field="max_infiltration_capacity_file" index="5" name=""/>
    <alias field="display_name" index="6" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1,maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="infiltration_rate"/>
    <default expression="" applyOnUpdate="0" field="infiltration_rate_file"/>
    <default expression="0" applyOnUpdate="0" field="infiltration_surface_option"/>
    <default expression="" applyOnUpdate="0" field="max_infiltration_capacity_file"/>
    <default expression="'new'" applyOnUpdate="0" field="display_name"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="infiltration_rate" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="infiltration_rate_file" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="infiltration_surface_option" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="max_infiltration_capacity_file" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="display_name" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="infiltration_rate"/>
    <constraint exp="" desc="" field="infiltration_rate_file"/>
    <constraint exp="" desc="" field="infiltration_surface_option"/>
    <constraint exp="" desc="" field="max_infiltration_capacity_file"/>
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
      <column width="-1" hidden="0" type="field" name="infiltration_rate"/>
      <column width="-1" hidden="0" type="field" name="infiltration_rate_file"/>
      <column width="-1" hidden="0" type="field" name="infiltration_surface_option"/>
      <column width="-1" hidden="0" type="field" name="max_infiltration_capacity_file"/>
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
      <attributeEditorField showLabel="1" index="6" name="display_name"/>
      <attributeEditorField showLabel="1" index="2" name="infiltration_rate"/>
      <attributeEditorField showLabel="1" index="3" name="infiltration_rate_file"/>
      <attributeEditorField showLabel="1" index="5" name="max_infiltration_capacity_file"/>
      <attributeEditorField showLabel="1" index="4" name="infiltration_surface_option"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="display_name"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltration_rate"/>
    <field editable="1" name="infiltration_rate_file"/>
    <field editable="1" name="infiltration_surface_option"/>
    <field editable="1" name="max_infiltration_capacity_file"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltration_rate"/>
    <field labelOnTop="0" name="infiltration_rate_file"/>
    <field labelOnTop="0" name="infiltration_surface_option"/>
    <field labelOnTop="0" name="max_infiltration_capacity_file"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
