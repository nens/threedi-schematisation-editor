<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" labelsEnabled="0" readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 type="singleSymbol" symbollevels="0" enableorderby="0" forceraster="0">
    <symbols>
      <symbol name="0" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
        <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
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
    <alias name="" field="fid" index="0"/>
    <alias name="" field="id" index="1"/>
    <alias name="" field="code" index="2"/>
    <alias name="" field="reference_level" index="3"/>
    <alias name="" field="friction_type" index="4"/>
    <alias name="" field="friction_value" index="5"/>
    <alias name="" field="bank_level" index="6"/>
    <alias name="" field="channel_id" index="7"/>
    <alias name="" field="cross_section_shape" index="8"/>
    <alias name="" field="cross_section_width" index="9"/>
    <alias name="" field="cross_section_height" index="10"/>
    <alias name="" field="cross_section_table" index="11"/>
  </aliases>
  <defaults>
    <default applyOnUpdate="0" expression="" field="fid"/>
    <default applyOnUpdate="0" expression="" field="id"/>
    <default applyOnUpdate="0" expression="" field="code"/>
    <default applyOnUpdate="0" expression="" field="reference_level"/>
    <default applyOnUpdate="0" expression="" field="friction_type"/>
    <default applyOnUpdate="0" expression="" field="friction_value"/>
    <default applyOnUpdate="0" expression="" field="bank_level"/>
    <default applyOnUpdate="0" expression="" field="channel_id"/>
    <default applyOnUpdate="0" expression="" field="cross_section_shape"/>
    <default applyOnUpdate="0" expression="" field="cross_section_width"/>
    <default applyOnUpdate="0" expression="" field="cross_section_height"/>
    <default applyOnUpdate="0" expression="" field="cross_section_table"/>
  </defaults>
  <constraints>
    <constraint unique_strength="1" exp_strength="0" field="fid" notnull_strength="1" constraints="3"/>
    <constraint unique_strength="0" exp_strength="0" field="id" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="code" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="reference_level" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="friction_type" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="friction_value" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="bank_level" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="channel_id" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cross_section_shape" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cross_section_width" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cross_section_height" notnull_strength="0" constraints="0"/>
    <constraint unique_strength="0" exp_strength="0" field="cross_section_table" notnull_strength="0" constraints="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" field="fid" exp=""/>
    <constraint desc="" field="id" exp=""/>
    <constraint desc="" field="code" exp=""/>
    <constraint desc="" field="reference_level" exp=""/>
    <constraint desc="" field="friction_type" exp=""/>
    <constraint desc="" field="friction_value" exp=""/>
    <constraint desc="" field="bank_level" exp=""/>
    <constraint desc="" field="channel_id" exp=""/>
    <constraint desc="" field="cross_section_shape" exp=""/>
    <constraint desc="" field="cross_section_width" exp=""/>
    <constraint desc="" field="cross_section_height" exp=""/>
    <constraint desc="" field="cross_section_table" exp=""/>
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
    <attributeEditorContainer name="Cross section location view" groupBox="0" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" showLabel="1">
      <attributeEditorContainer name="General" groupBox="1" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" showLabel="1">
        <attributeEditorField name="id" index="1" showLabel="1"/>
        <attributeEditorField name="code" index="2" showLabel="1"/>
        <attributeEditorField name="reference_level" index="3" showLabel="1"/>
        <attributeEditorField name="bank_level" index="6" showLabel="1"/>
        <attributeEditorField name="friction_type" index="4" showLabel="1"/>
        <attributeEditorField name="friction_value" index="5" showLabel="1"/>
        <attributeEditorField name="channel_id" index="7" showLabel="1"/>
      </attributeEditorContainer>
      <attributeEditorContainer name="Cross section" groupBox="1" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" showLabel="1">
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
