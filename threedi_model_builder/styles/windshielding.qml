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
    <field name="north" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="northeast" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="east" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="southeast" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
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
    <alias field="north" index="2" name=""/>
    <alias field="northeast" index="3" name=""/>
    <alias field="east" index="4" name=""/>
    <alias field="southeast" index="5" name=""/>
    <alias field="south" index="6" name=""/>
    <alias field="southwest" index="7" name=""/>
    <alias field="west" index="8" name=""/>
    <alias field="northwest" index="9" name=""/>
    <alias field="channel_id" index="10" name=""/>
  </aliases>
  <defaults>
    <default expression="" applyOnUpdate="0" field="fid"/>
    <default expression="if(maximum(id) is null,1, maximum(id)+1)" applyOnUpdate="0" field="id"/>
    <default expression="" applyOnUpdate="0" field="north"/>
    <default expression="" applyOnUpdate="0" field="northeast"/>
    <default expression="" applyOnUpdate="0" field="east"/>
    <default expression="" applyOnUpdate="0" field="southeast"/>
    <default expression="" applyOnUpdate="0" field="south"/>
    <default expression="" applyOnUpdate="0" field="southwest"/>
    <default expression="" applyOnUpdate="0" field="west"/>
    <default expression="" applyOnUpdate="0" field="northwest"/>
    <default expression="" applyOnUpdate="0" field="channel_id"/>
  </defaults>
  <constraints>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="fid" unique_strength="1"/>
    <constraint constraints="3" exp_strength="0" notnull_strength="1" field="id" unique_strength="1"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="north" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="northeast" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="east" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="southeast" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="south" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="southwest" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="west" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="northwest" unique_strength="0"/>
    <constraint constraints="0" exp_strength="0" notnull_strength="0" field="channel_id" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="north"/>
    <constraint exp="" desc="" field="northeast"/>
    <constraint exp="" desc="" field="east"/>
    <constraint exp="" desc="" field="southeast"/>
    <constraint exp="" desc="" field="south"/>
    <constraint exp="" desc="" field="southwest"/>
    <constraint exp="" desc="" field="west"/>
    <constraint exp="" desc="" field="northwest"/>
    <constraint exp="" desc="" field="channel_id"/>
  </constraintExpressions>
  <expressionfields/>
  <attributeactions>
    <defaultAction value="{00000000-0000-0000-0000-000000000000}" key="Canvas"/>
  </attributeactions>
  <attributetableconfig sortOrder="0" sortExpression="" actionWidgetStyle="dropDown">
    <columns>
      <column width="-1" hidden="1" type="field" name="fid"/>
      <column width="-1" hidden="0" type="field" name="id"/>
      <column width="-1" hidden="0" type="field" name="north"/>
      <column width="-1" hidden="0" type="field" name="northeast"/>
      <column width="-1" hidden="0" type="field" name="east"/>
      <column width="-1" hidden="0" type="field" name="southeast"/>
      <column width="-1" hidden="0" type="field" name="south"/>
      <column width="-1" hidden="0" type="field" name="southwest"/>
      <column width="-1" hidden="0" type="field" name="west"/>
      <column width="-1" hidden="0" type="field" name="northwest"/>
      <column width="-1" hidden="0" type="field" name="channel_id"/>
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
      <attributeEditorField showLabel="1" index="10" name="channel_id"/>
      <attributeEditorField showLabel="1" index="2" name="north"/>
      <attributeEditorField showLabel="1" index="3" name="northeast"/>
      <attributeEditorField showLabel="1" index="4" name="east"/>
      <attributeEditorField showLabel="1" index="5" name="southeast"/>
      <attributeEditorField showLabel="1" index="6" name="south"/>
      <attributeEditorField showLabel="1" index="7" name="southwest"/>
      <attributeEditorField showLabel="1" index="8" name="west"/>
      <attributeEditorField showLabel="1" index="9" name="northwest"/>
      <attributeEditorField showLabel="1" index="-1" name="the_geom"/>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="east"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="id"/>
    <field editable="1" name="north"/>
    <field editable="1" name="northeast"/>
    <field editable="1" name="northwest"/>
    <field editable="1" name="south"/>
    <field editable="1" name="southeast"/>
    <field editable="1" name="southwest"/>
    <field editable="1" name="the_geom"/>
    <field editable="1" name="west"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="east"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="north"/>
    <field labelOnTop="0" name="northeast"/>
    <field labelOnTop="0" name="northwest"/>
    <field labelOnTop="0" name="south"/>
    <field labelOnTop="0" name="southeast"/>
    <field labelOnTop="0" name="southwest"/>
    <field labelOnTop="0" name="the_geom"/>
    <field labelOnTop="0" name="west"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <mapTip></mapTip>
  <layerGeometryType>4</layerGeometryType>
</qgis>
