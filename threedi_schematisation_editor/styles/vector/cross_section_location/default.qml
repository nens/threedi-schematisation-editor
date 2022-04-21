<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="diamond"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="area"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="MM"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties" type="Map">
                <Option name="size" type="Map">
                  <Option name="active" type="bool" value="true"/>
                  <Option name="expression" type="QString" value="if(@map_scale&lt;10000, 2,0.5)"/>
                  <Option name="type" type="int" value="3"/>
                </Option>
              </Option>
              <Option name="type" type="QString" value="collection"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field name="fid" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field name="id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="int" value="2147483647"/>
            <Option name="Min" type="int" value="-2147483648"/>
            <Option name="Precision" type="int" value="0"/>
            <Option name="Step" type="int" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reference_level" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="1.7976931348623157e+308"/>
            <Option name="Min" type="double" value="-1.7976931348623157e+308"/>
            <Option name="Precision" type="int" value="3"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="1: Chèzy" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Manning" type="QString" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_value" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="1.7976931348623157e+308"/>
            <Option name="Min" type="double" value="-1.7976931348623157e+308"/>
            <Option name="Precision" type="int" value="3"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="int" value="2147483647"/>
            <Option name="Min" type="int" value="-2147483648"/>
            <Option name="Precision" type="int" value="0"/>
            <Option name="Step" type="int" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_shape" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Circle" type="QString" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="Egg" type="QString" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="Rectangle" type="QString" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated rectangle" type="QString" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated trapezium" type="QString" value="6"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_width" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="1.7976931348623157e+308"/>
            <Option name="Min" type="double" value="-1.7976931348623157e+308"/>
            <Option name="Precision" type="int" value="3"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_height" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option name="AllowNull" type="bool" value="true"/>
            <Option name="Max" type="double" value="1.7976931348623157e+308"/>
            <Option name="Min" type="double" value="-1.7976931348623157e+308"/>
            <Option name="Precision" type="int" value="3"/>
            <Option name="Step" type="double" value="1"/>
            <Option name="Style" type="QString" value="SpinBox"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_table" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="true"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias name="" index="0" field="fid"/>
    <alias name="" index="1" field="id"/>
    <alias name="" index="2" field="code"/>
    <alias name="" index="3" field="reference_level"/>
    <alias name="" index="4" field="friction_type"/>
    <alias name="" index="5" field="friction_value"/>
    <alias name="" index="6" field="bank_level"/>
    <alias name="" index="7" field="channel_id"/>
    <alias name="" index="8" field="cross_section_shape"/>
    <alias name="" index="9" field="cross_section_width"/>
    <alias name="" index="10" field="cross_section_height"/>
    <alias name="" index="11" field="cross_section_table"/>
  </aliases>
  <defaults>
    <default field="fid" applyOnUpdate="0" expression=""/>
    <default field="id" applyOnUpdate="0" expression=""/>
    <default field="code" applyOnUpdate="0" expression=""/>
    <default field="reference_level" applyOnUpdate="0" expression=""/>
    <default field="friction_type" applyOnUpdate="0" expression=""/>
    <default field="friction_value" applyOnUpdate="0" expression=""/>
    <default field="bank_level" applyOnUpdate="0" expression=""/>
    <default field="channel_id" applyOnUpdate="0" expression=""/>
    <default field="cross_section_shape" applyOnUpdate="0" expression=""/>
    <default field="cross_section_width" applyOnUpdate="0" expression=""/>
    <default field="cross_section_height" applyOnUpdate="0" expression=""/>
    <default field="cross_section_table" applyOnUpdate="0" expression=""/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" notnull_strength="1" constraints="3" field="fid" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="id" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="code" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="reference_level" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="friction_type" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="friction_value" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="bank_level" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="channel_id" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="cross_section_shape" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="cross_section_width" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="cross_section_height" exp_strength="0"/>
    <constraint unique_strength="0" notnull_strength="0" constraints="0" field="cross_section_table" exp_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint exp="" desc="" field="fid"/>
    <constraint exp="" desc="" field="id"/>
    <constraint exp="" desc="" field="code"/>
    <constraint exp="" desc="" field="reference_level"/>
    <constraint exp="" desc="" field="friction_type"/>
    <constraint exp="" desc="" field="friction_value"/>
    <constraint exp="" desc="" field="bank_level"/>
    <constraint exp="" desc="" field="channel_id"/>
    <constraint exp="" desc="" field="cross_section_shape"/>
    <constraint exp="" desc="" field="cross_section_width"/>
    <constraint exp="" desc="" field="cross_section_height"/>
    <constraint exp="" desc="" field="cross_section_table"/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_schematisation_editor\forms\ui\cross_section_location.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_schematisation_editor.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer name="Cross section location view" visibilityExpression="" showLabel="1" groupBox="0" visibilityExpressionEnabled="0" columnCount="1">
      <attributeEditorContainer name="General" visibilityExpression="" showLabel="1" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField name="id" index="1" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
        <attributeEditorField name="reference_level" index="3" showLabel="1"/>
        <attributeEditorField name="bank_level" index="6" showLabel="1"/>
        <attributeEditorField name="friction_type" index="4" showLabel="1"/>
        <attributeEditorField name="friction_value" index="5" showLabel="1"/>
        <attributeEditorField name="channel_id" index="7" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section" visibilityExpression="" showLabel="1" groupBox="1" visibilityExpressionEnabled="0" columnCount="1">
        <attributeEditorField name="cross_section_shape" index="8" showLabel="1"/>
        <attributeEditorField name="cross_section_height" index="10" showLabel="1"/>
        <attributeEditorField name="cross_section_width" index="9" showLabel="1"/>
        <attributeEditorField name="cross_section_table" index="11" showLabel="1"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field name="Cross section definition_height" editable="0"/>
    <field name="Cross section definition_shape" editable="0"/>
    <field name="Cross section definition_width" editable="0"/>
    <field name="ROWID" editable="1"/>
    <field name="bank_level" editable="1"/>
    <field name="channel_id" editable="1"/>
    <field name="code" editable="1"/>
    <field name="cross_section_height" editable="1"/>
    <field name="cross_section_shape" editable="1"/>
    <field name="cross_section_table" editable="1"/>
    <field name="cross_section_width" editable="1"/>
    <field name="definition_id" editable="1"/>
    <field name="fid" editable="1"/>
    <field name="friction_type" editable="1"/>
    <field name="friction_value" editable="1"/>
    <field name="id" editable="1"/>
    <field name="reference_level" editable="1"/>
  </editable>
  <labelOnTop>
    <field name="Cross section definition_height" labelOnTop="0"/>
    <field name="Cross section definition_shape" labelOnTop="0"/>
    <field name="Cross section definition_width" labelOnTop="0"/>
    <field name="ROWID" labelOnTop="0"/>
    <field name="bank_level" labelOnTop="0"/>
    <field name="channel_id" labelOnTop="0"/>
    <field name="code" labelOnTop="0"/>
    <field name="cross_section_height" labelOnTop="0"/>
    <field name="cross_section_shape" labelOnTop="0"/>
    <field name="cross_section_table" labelOnTop="0"/>
    <field name="cross_section_width" labelOnTop="0"/>
    <field name="definition_id" labelOnTop="0"/>
    <field name="fid" labelOnTop="0"/>
    <field name="friction_type" labelOnTop="0"/>
    <field name="friction_value" labelOnTop="0"/>
    <field name="id" labelOnTop="0"/>
    <field name="reference_level" labelOnTop="0"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"fid"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
