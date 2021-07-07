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
    <field name="global_settings_id" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="var_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="flow_variable" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="discharge" type="QString" name="discharge"/>
              </Option>
              <Option type="Map">
                <Option value="flow_velocity" type="QString" name="flow velocity"/>
              </Option>
              <Option type="Map">
                <Option value="pump_discharge" type="QString" name="pump discharge"/>
              </Option>
              <Option type="Map">
                <Option value="rain" type="QString" name="rain"/>
              </Option>
              <Option type="Map">
                <Option value="waterlevel" type="QString" name="waterlevel"/>
              </Option>
              <Option type="Map">
                <Option value="wet_cross-section" type="QString" name="wet cross section"/>
              </Option>
              <Option type="Map">
                <Option value="wet_surface" type="QString" name="wet surface"/>
              </Option>
              <Option type="Map">
                <Option value="lateral_discharge" type="QString" name="lateral discharge"/>
              </Option>
              <Option type="Map">
                <Option value="volume" type="QString" name="volume"/>
              </Option>
              <Option type="Map">
                <Option value="simple_infiltration" type="QString" name="infiltration"/>
              </Option>
              <Option type="Map">
                <Option value="leakage" type="QString" name="leakage"/>
              </Option>
              <Option type="Map">
                <Option value="interception" type="QString" name="interception"/>
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
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="avg" type="QString" name="average"/>
              </Option>
              <Option type="Map">
                <Option value="min" type="QString" name="minimum"/>
              </Option>
              <Option type="Map">
                <Option value="max" type="QString" name="maximum"/>
              </Option>
              <Option type="Map">
                <Option value="cum" type="QString" name="cumulative"/>
              </Option>
              <Option type="Map">
                <Option value="med" type="QString" name="median"/>
              </Option>
              <Option type="Map">
                <Option value="cum_negative" type="QString" name="cumulative negative"/>
              </Option>
              <Option type="Map">
                <Option value="cum_positive" type="QString" name="cumulative positive"/>
              </Option>
              <Option type="Map">
                <Option value="current" type="QString" name="current"/>
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
    <alias field="global_settings_id" index="2" name=""/>
    <alias field="var_name" index="3" name=""/>
    <alias field="flow_variable" index="4" name=""/>
    <alias field="aggregation_method" index="5" name=""/>
    <alias field="aggregation_in_space" index="6" name=""/>
    <alias field="timestep" index="7" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="global_settings_id"/>
    <default expression="" applyOnUpdate="0" field="var_name"/>
    <default expression="" applyOnUpdate="0" field="flow_variable"/>
    <default expression="" applyOnUpdate="0" field="aggregation_method"/>
    <default expression="0" applyOnUpdate="0" field="aggregation_in_space"/>
    <default expression="" applyOnUpdate="0" field="timestep"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="global_settings_id" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="var_name" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="flow_variable" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="aggregation_method" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="aggregation_in_space" unique_strength="0"/>
    <constraint constraints="1" exp_strength="0" notnull_strength="2" field="timestep" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="global_settings_id"/>
    <constraint exp="" desc="" field="var_name"/>
    <constraint exp="" desc="" field="flow_variable"/>
    <constraint exp="" desc="" field="aggregation_method"/>
    <constraint exp="" desc="" field="aggregation_in_space"/>
    <constraint exp="" desc="" field="timestep"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="global_settings_id"/>
      <column width="-1" hidden="0" type="field" name="var_name"/>
      <column width="-1" hidden="0" type="field" name="flow_variable"/>
      <column width="-1" hidden="0" type="field" name="aggregation_method"/>
      <column width="-1" hidden="0" type="field" name="aggregation_in_space"/>
      <column width="-1" hidden="0" type="field" name="timestep"/>
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
      <attributeEditorField showLabel="1" index="4" name="flow_variable"/>
      <attributeEditorField showLabel="1" index="5" name="aggregation_method"/>
      <attributeEditorField showLabel="1" index="7" name="timestep"/>
      <attributeEditorField showLabel="1" index="3" name="var_name"/>
      <attributeEditorField showLabel="1" index="2" name="global_settings_id"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="aggregation_in_space"/>
    <field editable="1" name="aggregation_method"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="flow_variable"/>
    <field editable="1" name="global_settings_id"/>
    <field editable="1" name="id"/>
    <field editable="1" name="timestep"/>
    <field editable="1" name="var_name"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="aggregation_in_space"/>
    <field labelOnTop="0" name="aggregation_method"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="flow_variable"/>
    <field labelOnTop="0" name="global_settings_id"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="timestep"/>
    <field labelOnTop="0" name="var_name"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"var_name"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
