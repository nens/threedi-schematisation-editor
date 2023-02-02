<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" version="3.22.11-Białowieża" minScale="0" maxScale="0" styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
    <Private>0</Private>
  </flags>
  <temporal endExpression="" durationField="" startField="" accumulate="0" limitMode="0" fixedDuration="0" mode="0" enabled="0" endField="" startExpression="" durationUnit="min">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <Option type="Map">
      <Option type="List" name="dualview/previewExpressions">
        <Option type="QString" value="&quot;id&quot;"/>
      </Option>
      <Option type="QString" name="embeddedWidgets/count" value="0"/>
      <Option name="variableNames"/>
      <Option name="variableValues"/>
    </Option>
  </customproperties>
  <geometryOptions geometryPrecision="0" removeDuplicateNodes="0">
    <activeChecks/>
    <checkConfiguration/>
  </geometryOptions>
  <legend showLabelLegend="0" type="default-vector"/>
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
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="1.7976931348623157e+308"/>
            <Option type="double" name="Min" value="-1.7976931348623157e+308"/>
            <Option type="int" name="Precision" value="3"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_rate_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="infiltration_surface_option" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option type="QString" name="" value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Rain" value="0"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Whole surface" value="1"/>
              </Option>
              <Option type="Map">
                <Option type="QString" name="Wet surface" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity_file" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="display_name" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option type="bool" name="IsMultiline" value="false"/>
            <Option type="bool" name="UseHtml" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="max_infiltration_capacity" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option type="bool" name="AllowNull" value="true"/>
            <Option type="double" name="Max" value="1.7976931348623157e+308"/>
            <Option type="double" name="Min" value="-1.7976931348623157e+308"/>
            <Option type="int" name="Precision" value="3"/>
            <Option type="double" name="Step" value="1"/>
            <Option type="QString" name="Style" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="fid"/>
    <alias name="" index="1" field="id"/>
    <alias name="" index="2" field="infiltration_rate"/>
    <alias name="" index="3" field="infiltration_rate_file"/>
    <alias name="" index="4" field="infiltration_surface_option"/>
    <alias name="" index="5" field="max_infiltration_capacity_file"/>
    <alias name="" index="6" field="display_name"/>
    <alias name="" index="7" field="max_infiltration_capacity"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="fid"/>
    <default applyOnUpdate="0" expression="if (maximum(id) is null, 1, maximum(id) + 1)" field="id"/>
    <default applyOnUpdate="0" expression="" field="infiltration_rate"/>
    <default applyOnUpdate="0" expression="" field="infiltration_rate_file"/>
    <default applyOnUpdate="0" expression="0" field="infiltration_surface_option"/>
    <default applyOnUpdate="0" expression="" field="max_infiltration_capacity_file"/>
    <default applyOnUpdate="0" expression="'new'" field="display_name"/>
    <default applyOnUpdate="0" expression="" field="max_infiltration_capacity"/>
  </defaults>
  <constraints>
    <constraint constraints="3" unique_strength="1" exp_strength="0" notnull_strength="1" field="fid"/>
    <constraint constraints="3" unique_strength="1" exp_strength="0" notnull_strength="1" field="id"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" notnull_strength="2" field="infiltration_rate"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" notnull_strength="0" field="infiltration_rate_file"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" notnull_strength="0" field="infiltration_surface_option"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" notnull_strength="0" field="max_infiltration_capacity_file"/>
    <constraint constraints="1" unique_strength="0" exp_strength="0" notnull_strength="2" field="display_name"/>
    <constraint constraints="0" unique_strength="0" exp_strength="0" notnull_strength="0" field="max_infiltration_capacity"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="infiltration_rate"/>
    <constraint desc="" exp="" field="infiltration_rate_file"/>
    <constraint desc="" exp="" field="infiltration_surface_option"/>
    <constraint desc="" exp="" field="max_infiltration_capacity_file"/>
    <constraint desc="" exp="" field="display_name"/>
    <constraint desc="" exp="" field="max_infiltration_capacity"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction key="Canvas" value="{00000000-0000-0000-0000-000000000000}"/>
  </attributeactions>
  <attributetableconfig actionWidgetStyle="dropDown" sortOrder="0" sortExpression="">
    <columns>
      <column width="-1" type="field" name="fid" hidden="1"/>
      <column width="-1" type="field" name="id" hidden="0"/>
      <column width="-1" type="field" name="infiltration_rate" hidden="0"/>
      <column width="210" type="field" name="infiltration_rate_file" hidden="0"/>
      <column width="209" type="field" name="infiltration_surface_option" hidden="0"/>
      <column width="271" type="field" name="max_infiltration_capacity_file" hidden="0"/>
      <column width="196" type="field" name="display_name" hidden="0"/>
      <column width="-1" type="field" name="max_infiltration_capacity" hidden="0"/>
      <column width="-1" type="actions" hidden="1"/>
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
    <attributeEditorContainer groupBox="0" showLabel="1" name="General" visibilityExpressionEnabled="0" columnCount="1" visibilityExpression="">
      <attributeEditorField showLabel="1" name="id" index="1"/>
      <attributeEditorField showLabel="1" name="display_name" index="6"/>
      <attributeEditorField showLabel="1" name="infiltration_rate" index="2"/>
      <attributeEditorField showLabel="1" name="infiltration_rate_file" index="3"/>
      <attributeEditorField showLabel="1" name="max_infiltration_capacity" index="7"/>
      <attributeEditorField showLabel="1" name="max_infiltration_capacity_file" index="5"/>
      <attributeEditorField showLabel="1" name="infiltration_surface_option" index="4"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="display_name"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="infiltration_rate"/>
    <field editable="1" name="infiltration_rate_file"/>
    <field editable="1" name="infiltration_surface_option"/>
    <field editable="1" name="max_infiltration_capacity"/>
    <field editable="1" name="max_infiltration_capacity_file"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="display_name"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="infiltration_rate"/>
    <field labelOnTop="0" name="infiltration_rate_file"/>
    <field labelOnTop="0" name="infiltration_surface_option"/>
    <field labelOnTop="0" name="max_infiltration_capacity"/>
    <field labelOnTop="0" name="max_infiltration_capacity_file"/>
  </labelOnTop>
  <reuseLastValue>
    <field name="display_name" reuseLastValue="0"/>
    <field name="fid" reuseLastValue="0"/>
    <field name="id" reuseLastValue="0"/>
    <field name="infiltration_rate" reuseLastValue="0"/>
    <field name="infiltration_rate_file" reuseLastValue="0"/>
    <field name="infiltration_surface_option" reuseLastValue="0"/>
    <field name="max_infiltration_capacity" reuseLastValue="0"/>
    <field name="max_infiltration_capacity_file" reuseLastValue="0"/>
  </reuseLastValue>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
