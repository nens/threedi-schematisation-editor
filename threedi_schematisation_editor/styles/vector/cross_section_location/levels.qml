<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="1">
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
  <labeling type="simple">
    <settings calloutType="simple">
      <text-style blendMode="0" multilineHeight="1" namedStyle="Regular" textColor="0,0,0,255" fontWeight="50" fontSizeUnit="Point" isExpression="1" allowHtml="0" textOrientation="horizontal" capitalization="0" useSubstitutions="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontSize="7" fontWordSpacing="0" fontFamily="MS Gothic" fontItalic="0" previewBkgrdColor="255,255,255,255" fontStrikeout="0" fieldName="'bank: '|| coalesce(format_number(bank_level, 2),'NULL')|| '\n'  || &#xd;&#xa;'ref:'|| coalesce(format_number(reference_level, 2),'NULL') ||'\n'  || &#xd;&#xa;'diff:'|| coalesce(format_number(bank_level - reference_level, 2),'NULL')&#xd;&#xa;" fontKerning="1" fontLetterSpacing="0" textOpacity="1" fontUnderline="0">
        <text-buffer bufferBlendMode="0" bufferSizeUnits="MM" bufferSize="0.7" bufferNoFill="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferDraw="1" bufferJoinStyle="128" bufferOpacity="1"/>
        <text-mask maskSizeUnits="MM" maskOpacity="1" maskEnabled="0" maskSize="0" maskedSymbolLayers="" maskType="0" maskJoinStyle="128" maskSizeMapUnitScale="3x:0,0,0,0,0,0"/>
        <background shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeJoinStyle="64" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeOpacity="1" shapeSizeUnit="MM" shapeBorderWidth="0" shapeFillColor="255,255,255,255" shapeOffsetY="0" shapeRadiiUnit="MM" shapeRadiiX="0" shapeRotationType="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeType="0" shapeOffsetUnit="MM" shapeSizeX="0" shapeSVGFile="" shapeOffsetX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeDraw="0" shapeSizeY="0" shapeBlendMode="0" shapeRotation="0" shapeSizeType="0">
          <symbol name="markerSymbol" force_rhr="0" type="marker" alpha="1" clip_to_extent="1">
            <layer pass="0" enabled="1" class="SimpleMarker" locked="0">
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
        <shadow shadowRadius="1.5" shadowBlendMode="6" shadowDraw="0" shadowOpacity="0.7" shadowScale="100" shadowUnder="0" shadowOffsetUnit="MM" shadowRadiusAlphaOnly="0" shadowRadiusUnit="MM" shadowOffsetAngle="135" shadowOffsetDist="1" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowOffsetGlobal="1" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255"/>
        <dd_properties>
          <Option type="Map">
            <Option name="name" type="QString" value=""/>
            <Option name="properties"/>
            <Option name="type" type="QString" value="collection"/>
          </Option>
        </dd_properties>
        <substitutions/>
      </text-style>
      <text-format addDirectionSymbol="0" rightDirectionSymbol=">" wrapChar="" leftDirectionSymbol="&lt;" decimals="3" multilineAlign="2" useMaxLineLengthForAutoWrap="1" formatNumbers="0" placeDirectionSymbol="0" reverseDirectionSymbol="0" autoWrapLength="0" plussign="0"/>
      <placement offsetType="0" xOffset="0" dist="0" geometryGeneratorType="PointGeometry" maxCurvedCharAngleOut="-25" overrunDistance="0" lineAnchorType="0" distMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" overrunDistanceUnit="MM" lineAnchorPercent="0.5" yOffset="0" repeatDistance="0" layerType="PointGeometry" geometryGenerator="" maxCurvedCharAngleIn="25" offsetUnits="MapUnit" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" quadOffset="4" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" polygonPlacementFlags="2" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" placementFlags="9" repeatDistanceUnits="MM" rotationAngle="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" placement="0" centroidInside="0" preserveRotation="1" centroidWhole="0" distUnits="MM" geometryGeneratorEnabled="0" priority="5"/>
      <rendering drawLabels="1" scaleVisibility="1" maxNumLabels="2000" fontMinPixelSize="3" mergeLines="0" minFeatureSize="0" zIndex="0" obstacle="1" fontMaxPixelSize="10000" obstacleFactor="1" obstacleType="0" limitNumLabels="0" upsidedownLabels="0" scaleMin="1" scaleMax="5000" displayAll="0" labelPerPart="0" fontLimitPixelSize="0"/>
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
          <Option name="lineSymbol" type="QString" value="&lt;symbol name=&quot;symbol&quot; force_rhr=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot;>&lt;layer pass=&quot;0&quot; enabled=&quot;1&quot; class=&quot;SimpleLine&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
