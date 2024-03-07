<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" labelsEnabled="1" readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms">
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
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style previewBkgrdColor="255,255,255,255" fontWordSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSize="7" textOpacity="1" blendMode="0" fontSizeUnit="Point" fontKerning="1" fieldName="'bank: '|| coalesce(format_number(bank_level, 2),'NULL')|| '\n'  || &#xd;&#xa;'ref:'|| coalesce(format_number(reference_level, 2),'NULL') ||'\n'  || &#xd;&#xa;'diff:'|| coalesce(format_number(bank_level - reference_level, 2),'NULL')&#xd;&#xa;" fontWeight="50" fontFamily="MS Gothic" fontUnderline="0" allowHtml="0" useSubstitutions="0" isExpression="1" multilineHeight="1" namedStyle="Regular" fontItalic="0" textColor="0,0,0,255" fontLetterSpacing="0" fontStrikeout="0" capitalization="0" textOrientation="horizontal">
        <text-buffer bufferDraw="1" bufferColor="255,255,255,255" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferNoFill="0" bufferSizeUnits="MM" bufferOpacity="1" bufferBlendMode="0" bufferSize="0.7"/>
        <text-mask maskSize="0" maskJoinStyle="128" maskEnabled="0" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskedSymbolLayers="" maskType="0" maskSizeUnits="MM"/>
        <background shapeSizeX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiUnit="MM" shapeOffsetUnit="MM" shapeBlendMode="0" shapeSizeUnit="MM" shapeRotationType="0" shapeDraw="0" shapeSVGFile="" shapeSizeType="0" shapeFillColor="255,255,255,255" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeBorderWidth="0" shapeRadiiX="0" shapeSizeY="0" shapeOpacity="1" shapeOffsetY="0" shapeRotation="0" shapeBorderColor="128,128,128,255" shapeOffsetX="0" shapeJoinStyle="64" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM">
          <symbol name="markerSymbol" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
            <layer enabled="1" class="SimpleMarker" pass="0" locked="0">
              <prop k="angle" v="0"/>
              <prop k="color" v="133,182,111,255"/>
              <prop k="horizontal_anchor_point" v="1"/>
              <prop k="joinstyle" v="bevel"/>
              <prop k="name" v="circle"/>
              <prop k="offset" v="0,0"/>
              <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="offset_unit" v="MM"/>
              <prop k="outline_color" v="35,35,35,255"/>
              <prop k="outline_style" v="solid"/>
              <prop k="outline_width" v="0"/>
              <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="outline_width_unit" v="MM"/>
              <prop k="scale_method" v="diameter"/>
              <prop k="size" v="2"/>
              <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
              <prop k="size_unit" v="MM"/>
              <prop k="vertical_anchor_point" v="1"/>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" type="QString" value=""/>
                  <Option name="properties"/>
                  <Option name="type" type="QString" value="collection"/>
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowRadiusAlphaOnly="0" shadowDraw="0" shadowUnder="0" shadowOpacity="0.7" shadowBlendMode="6" shadowColor="0,0,0,255" shadowOffsetUnit="MM" shadowOffsetGlobal="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetAngle="135" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetDist="1" shadowRadius="1.5" shadowRadiusUnit="MM" shadowScale="100"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format rightDirectionSymbol=">" plussign="0" wrapChar="" useMaxLineLengthForAutoWrap="1" multilineAlign="2" reverseDirectionSymbol="0" placeDirectionSymbol="0" decimals="3" autoWrapLength="0" leftDirectionSymbol="&lt;" formatNumbers="0" addDirectionSymbol="0"/>
      <placement polygonPlacementFlags="2" centroidWhole="0" maxCurvedCharAngleOut="-25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" rotationAngle="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" dist="0" repeatDistance="0" layerType="PointGeometry" centroidInside="0" repeatDistanceUnits="MM" priority="5" offsetUnits="MapUnit" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" offsetType="0" placement="0" geometryGeneratorType="PointGeometry" fitInPolygonOnly="0" preserveRotation="1" yOffset="0" overrunDistanceUnit="MM" overrunDistance="0" xOffset="0" lineAnchorPercent="0.5" lineAnchorType="0" quadOffset="4" placementFlags="9" distUnits="MM" distMapUnitScale="3x:0,0,0,0,0,0" maxCurvedCharAngleIn="25" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0"/>
      <rendering scaleVisibility="1" fontLimitPixelSize="0" fontMinPixelSize="3" obstacleFactor="1" minFeatureSize="0" mergeLines="0" maxNumLabels="2000" displayAll="0" obstacleType="0" scaleMax="5000" fontMaxPixelSize="10000" obstacle="1" zIndex="0" labelPerPart="0" drawLabels="1" scaleMin="1" upsidedownLabels="0" limitNumLabels="0"/>
      <dd_properties>
        <Option type="Map">
          <Option name="name" type="QString" value=""/>
          <Option name="properties" type="Map">
            <Option name="Color" type="Map">
              <Option name="active" type="bool" value="false"/>
              <Option name="expression" type="QString" value="case &#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end"/>
              <Option name="type" type="int" value="3"/>
            </Option>
          </Option>
          <Option name="type" type="QString" value="collection"/>
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" type="QString" value="pole_of_inaccessibility"/>
          <Option name="ddProperties" type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
          <Option name="drawToAllParts" type="bool" value="false"/>
          <Option name="enabled" type="QString" value="0"/>
          <Option name="labelAnchorPoint" type="QString" value="point_on_exterior"/>
          <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer enabled=&quot;1&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
          <Option name="minLength" type="double" value="0"/>
          <Option name="minLengthMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="minLengthUnit" type="QString" value="MM"/>
          <Option name="offsetFromAnchor" type="double" value="0"/>
          <Option name="offsetFromAnchorMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromAnchorUnit" type="QString" value="MM"/>
          <Option name="offsetFromLabel" type="double" value="0"/>
          <Option name="offsetFromLabelMapUnitScale" type="QString" value="3x:0,0,0,0,0,0"/>
          <Option name="offsetFromLabelUnit" type="QString" value="MM"/>
        </Option>
      </callout>
    </settings>
  </labeling>
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
                <Option name="1: Chézy" type="QString" value="1"/>
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
                <Option name="0: Closed rectangle" type="int" value="0"/>
              </Option>
              <Option type="Map">
                <Option name="1: Open rectangle" type="int" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="2: Circle" type="int" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="3: Egg" type="int" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="5: Tabulated rectangle" type="int" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="6: Tabulated trapezium" type="int" value="6"/>
              </Option>
              <Option type="Map">
                <Option name="7: YZ" type="int" value="7"/>
              </Option>
              <Option type="Map">
                <Option name="8: Inverted egg" type="int" value="8"/>
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
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
