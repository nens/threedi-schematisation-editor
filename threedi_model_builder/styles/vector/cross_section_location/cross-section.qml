<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.16.9-Hannover" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="1" readOnly="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" enableorderby="0" type="singleSymbol" symbollevels="0">
    <symbols>
      <symbol type="marker" alpha="1" clip_to_extent="1" force_rhr="0" name="0">
        <layer pass="0" class="SimpleMarker" enabled="1" locked="0">
          <prop k="angle" v="0"/>
          <prop k="color" v="19,61,142,255"/>
          <prop k="horizontal_anchor_point" v="1"/>
          <prop k="joinstyle" v="bevel"/>
          <prop k="name" v="circle"/>
          <prop k="offset" v="0,0"/>
          <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="offset_unit" v="MM"/>
          <prop k="outline_color" v="0,0,0,255"/>
          <prop k="outline_style" v="solid"/>
          <prop k="outline_width" v="0"/>
          <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="outline_width_unit" v="MM"/>
          <prop k="scale_method" v="diameter"/>
          <prop k="size" v="2"/>
          <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
          <prop k="size_unit" v="RenderMetersInMapUnits"/>
          <prop k="vertical_anchor_point" v="1"/>
          <data_defined_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="size">
                  <Option value="true" type="bool" name="active"/>
                  <Option value="try(&#xd;&#xa;&#x9;coalesce(&#xd;&#xa;&#x9;&#x9;CASE WHEN cross_section_shape = 1 THEN to_real(cross_section_width)&#xd;&#xa;&#x9;&#x9;WHEN cross_section_shape = 2 THEN to_real(cross_section_width) &#xd;&#xa;&#x9;&#x9;WHEN cross_section_shape = 3 THEN to_real(cross_section_width)&#xd;&#xa;&#x9;&#x9;WHEN cross_section_shape in (5, 6) THEN &#xd;&#xa;&#x9;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;cross_section_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;END, &#xd;&#xa; &#x9;&#x9;1&#xd;&#xa;&#x9;), &#xd;&#xa;&#x9;1&#xd;&#xa;)" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </data_defined_properties>
        </layer>
      </symbol>
    </symbols>
    <rotation/>
    <sizescale/>
  </renderer-v2>
  <labeling type="rule-based">
    <rules key="{6a133481-53dc-4ebd-8c8e-42fc675f8422}">
      <rule scalemaxdenom="10000" key="{0b85f86e-c819-40a3-8114-9ee77cdfab21}" description="Crosssection">
        <settings calloutType="simple">
          <text-style allowHtml="0" isExpression="1" namedStyle="Regular" fontStrikeout="0" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" fontWordSpacing="0" useSubstitutions="0" fontKerning="1" fontUnderline="0" fontSize="7" multilineHeight="1" blendMode="0" fieldName="represent_value(cross_section_shape)&#xd;&#xa;|| '\n' || &#xd;&#xa;CASE WHEN cross_section_shape = 1 THEN 'w: '||format_number(to_real(cross_section_width),2) &#xd;&#xa;WHEN cross_section_shape = 2 THEN 'Ø'||format_number(to_real(cross_section_width),2) &#xd;&#xa;WHEN cross_section_shape = 3 THEN 'w: ' || format_number(to_real(cross_section_width),2) &#xd;&#xa;WHEN cross_section_shape in (5, 6) THEN &#xd;&#xa;&#x9;'w: ' || &#xd;&#xa;&#x9;format_number(&#xd;&#xa;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;cross_section_width,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;2&#xd;&#xa;&#x9;)&#xd;&#xa;END&#xd;&#xa;||  '\n' || &#xd;&#xa;CASE WHEN cross_section_shape = 1 THEN 'h: '||format_number(to_real(cross_section_height),2) &#xd;&#xa;WHEN cross_section_shape = 2 THEN '' &#xd;&#xa;WHEN cross_section_shape = 3 THEN 'h: ' || format_number(to_real(cross_section_width*1.5),2) &#xd;&#xa;WHEN cross_section_shape in (5, 6) THEN &#xd;&#xa;&#x9;'h: ' || &#xd;&#xa;&#x9;format_number(&#xd;&#xa;&#x9;&#x9;to_real(&#xd;&#xa;&#x9;&#x9;&#x9;array_last(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;array_sort(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;string_to_array(&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;cross_section_height,&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;&#x9;' '&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;&#x9;)&#xd;&#xa;&#x9;&#x9;),&#xd;&#xa;&#x9;&#x9;2&#xd;&#xa;&#x9;)&#xd;&#xa;END" fontSizeUnit="Point" textOrientation="horizontal" capitalization="0" fontFamily="MS Gothic" fontWeight="50" fontSizeMapUnitScale="3x:0,0,0,0,0,0" fontLetterSpacing="0" textOpacity="1" fontItalic="0">
            <text-buffer bufferSize="0.7" bufferOpacity="1" bufferBlendMode="0" bufferSizeUnits="MM" bufferDraw="1" bufferColor="255,255,255,255" bufferNoFill="0" bufferJoinStyle="128" bufferSizeMapUnitScale="3x:0,0,0,0,0,0"/>
            <text-mask maskSizeUnits="MM" maskEnabled="0" maskType="0" maskSize="0" maskedSymbolLayers="" maskJoinStyle="128" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0"/>
            <background shapeSVGFile="" shapeOpacity="1" shapeType="0" shapeSizeUnit="MM" shapeOffsetY="0" shapeBlendMode="0" shapeRadiiUnit="MM" shapeRotationType="0" shapeRotation="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBorderColor="128,128,128,255" shapeDraw="0" shapeBorderWidthUnit="MM" shapeSizeType="0" shapeRadiiX="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeFillColor="255,255,255,255" shapeJoinStyle="64" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeSizeX="0" shapeOffsetUnit="MM" shapeOffsetX="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidth="0">
              <symbol type="marker" alpha="1" clip_to_extent="1" force_rhr="0" name="markerSymbol">
                <layer pass="0" class="SimpleMarker" enabled="1" locked="0">
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
                      <Option value="" type="QString" name="name"/>
                      <Option name="properties"/>
                      <Option value="collection" type="QString" name="type"/>
                    </Option>
                  </data_defined_properties>
                </layer>
              </symbol>
            </background>
            <shadow shadowUnder="0" shadowRadius="1.5" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowDraw="0" shadowOffsetGlobal="1" shadowColor="0,0,0,255" shadowOffsetAngle="135" shadowOffsetDist="1" shadowOpacity="0.7" shadowScale="100" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusAlphaOnly="0" shadowBlendMode="6" shadowRadiusUnit="MM" shadowOffsetUnit="MM"/>
            <dd_properties>
              <Option type="Map">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format useMaxLineLengthForAutoWrap="1" autoWrapLength="0" addDirectionSymbol="0" wrapChar="" decimals="3" rightDirectionSymbol=">" leftDirectionSymbol="&lt;" multilineAlign="0" plussign="0" reverseDirectionSymbol="0" placeDirectionSymbol="0" formatNumbers="0"/>
          <placement overrunDistanceUnit="MM" lineAnchorPercent="0.5" repeatDistance="0" polygonPlacementFlags="2" centroidInside="0" layerType="PointGeometry" preserveRotation="1" placement="0" geometryGenerator="" maxCurvedCharAngleOut="-25" geometryGeneratorType="PointGeometry" distMapUnitScale="3x:0,0,0,0,0,0" offsetType="0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" overrunDistance="0" fitInPolygonOnly="0" repeatDistanceUnits="MM" distUnits="MM" lineAnchorType="0" centroidWhole="0" maxCurvedCharAngleIn="25" offsetUnits="MapUnit" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" yOffset="0" xOffset="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" rotationAngle="0" priority="5" quadOffset="4" dist="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" placementFlags="9"/>
          <rendering fontMinPixelSize="3" upsidedownLabels="0" scaleMax="10000000" obstacle="1" fontMaxPixelSize="10000" scaleVisibility="0" zIndex="0" scaleMin="1" obstacleFactor="1" fontLimitPixelSize="0" displayAll="0" maxNumLabels="2000" minFeatureSize="0" drawLabels="1" mergeLines="0" obstacleType="0" labelPerPart="0" limitNumLabels="0"/>
          <dd_properties>
            <Option type="Map">
              <Option value="" type="QString" name="name"/>
              <Option type="Map" name="properties">
                <Option type="Map" name="Color">
                  <Option value="false" type="bool" name="active"/>
                  <Option value="case &#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ffaa00'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#55aaff'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#ff0000'&#xd;&#xa;when &quot;sewerage_type&quot; = 0 then '#999999'&#xd;&#xa;else '#000000'&#xd;&#xa;end" type="QString" name="expression"/>
                  <Option value="3" type="int" name="type"/>
                </Option>
              </Option>
              <Option value="collection" type="QString" name="type"/>
            </Option>
          </dd_properties>
          <callout type="simple">
            <Option type="Map">
              <Option value="pole_of_inaccessibility" type="QString" name="anchorPoint"/>
              <Option type="Map" name="ddProperties">
                <Option value="" type="QString" name="name"/>
                <Option name="properties"/>
                <Option value="collection" type="QString" name="type"/>
              </Option>
              <Option value="false" type="bool" name="drawToAllParts"/>
              <Option value="0" type="QString" name="enabled"/>
              <Option value="point_on_exterior" type="QString" name="labelAnchorPoint"/>
              <Option value="&lt;symbol type=&quot;line&quot; alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot;>&lt;layer pass=&quot;0&quot; class=&quot;SimpleLine&quot; enabled=&quot;1&quot; locked=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option value=&quot;&quot; type=&quot;QString&quot; name=&quot;name&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option value=&quot;collection&quot; type=&quot;QString&quot; name=&quot;type&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>" type="QString" name="lineSymbol"/>
              <Option value="0" type="double" name="minLength"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="minLengthMapUnitScale"/>
              <Option value="MM" type="QString" name="minLengthUnit"/>
              <Option value="0" type="double" name="offsetFromAnchor"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromAnchorMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromAnchorUnit"/>
              <Option value="0" type="double" name="offsetFromLabel"/>
              <Option value="3x:0,0,0,0,0,0" type="QString" name="offsetFromLabelMapUnitScale"/>
              <Option value="MM" type="QString" name="offsetFromLabelUnit"/>
            </Option>
          </callout>
        </settings>
      </rule>
    </rules>
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
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="code" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="reference_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="friction_type" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Chèzy"/>
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Manning"/>
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
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="bank_level" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="channel_id" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="2147483647" type="int" name="Max"/>
            <Option value="-2147483648" type="int" name="Min"/>
            <Option value="0" type="int" name="Precision"/>
            <Option value="1" type="int" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_shape" configurationFlags="None">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="2" type="QString" name="Circle"/>
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="Egg"/>
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="Rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="Tabulated rectangle"/>
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="Tabulated trapezium"/>
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
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="3" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_height" configurationFlags="None">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull"/>
            <Option value="1.7976931348623157e+308" type="double" name="Max"/>
            <Option value="-1.7976931348623157e+308" type="double" name="Min"/>
            <Option value="3" type="int" name="Precision"/>
            <Option value="1" type="double" name="Step"/>
            <Option value="SpinBox" type="QString" name="Style"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field name="cross_section_table" configurationFlags="None">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline"/>
            <Option value="false" type="bool" name="UseHtml"/>
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  <aliases>
    <alias field="fid" index="0" name=""/>
    <alias field="id" index="1" name=""/>
    <alias field="code" index="2" name=""/>
    <alias field="reference_level" index="3" name=""/>
    <alias field="friction_type" index="4" name=""/>
    <alias field="friction_value" index="5" name=""/>
    <alias field="bank_level" index="6" name=""/>
    <alias field="channel_id" index="7" name=""/>
    <alias field="cross_section_shape" index="8" name=""/>
    <alias field="cross_section_width" index="9" name=""/>
    <alias field="cross_section_height" index="10" name=""/>
    <alias field="cross_section_table" index="11" name=""/>
  </aliases>
  <defaults>
    <default expression="" field="fid" applyOnUpdate="0"/>
    <default expression="" field="id" applyOnUpdate="0"/>
    <default expression="" field="code" applyOnUpdate="0"/>
    <default expression="" field="reference_level" applyOnUpdate="0"/>
    <default expression="" field="friction_type" applyOnUpdate="0"/>
    <default expression="" field="friction_value" applyOnUpdate="0"/>
    <default expression="" field="bank_level" applyOnUpdate="0"/>
    <default expression="" field="channel_id" applyOnUpdate="0"/>
    <default expression="" field="cross_section_shape" applyOnUpdate="0"/>
    <default expression="" field="cross_section_width" applyOnUpdate="0"/>
    <default expression="" field="cross_section_height" applyOnUpdate="0"/>
    <default expression="" field="cross_section_table" applyOnUpdate="0"/>
  </defaults>
  <constraints>
    <constraint exp_strength="0" field="fid" constraints="3" unique_strength="1" notnull_strength="1"/>
    <constraint exp_strength="0" field="id" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="code" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="reference_level" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="friction_type" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="friction_value" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="bank_level" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="channel_id" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_shape" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_width" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_height" constraints="0" unique_strength="0" notnull_strength="0"/>
    <constraint exp_strength="0" field="cross_section_table" constraints="0" unique_strength="0" notnull_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint field="fid" desc="" exp=""/>
    <constraint field="id" desc="" exp=""/>
    <constraint field="code" desc="" exp=""/>
    <constraint field="reference_level" desc="" exp=""/>
    <constraint field="friction_type" desc="" exp=""/>
    <constraint field="friction_value" desc="" exp=""/>
    <constraint field="bank_level" desc="" exp=""/>
    <constraint field="channel_id" desc="" exp=""/>
    <constraint field="cross_section_shape" desc="" exp=""/>
    <constraint field="cross_section_width" desc="" exp=""/>
    <constraint field="cross_section_height" desc="" exp=""/>
    <constraint field="cross_section_table" desc="" exp=""/>
  </constraintExpressions>
  <expressionfields/>
  <editform tolerant="1">C:/Users/lukas/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\threedi_model_builder\forms\ui\cross_section_location.ui</editform>
  <editforminit>open_edit_form</editforminit>
  <editforminitcodesource>2</editforminitcodesource>
  <editforminitfilepath>.</editforminitfilepath>
  <editforminitcode><![CDATA[from threedi_model_builder.utils import open_edit_form]]></editforminitcode>
  <featformsuppress>0</featformsuppress>
  <editorlayout>uifilelayout</editorlayout>
  <attributeEditorForm>
    <attributeEditorContainer columnCount="1" groupBox="0" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="Cross section location view">
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="General">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="reference_level"/>
        <attributeEditorField showLabel="1" index="6" name="bank_level"/>
        <attributeEditorField showLabel="1" index="4" name="friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="friction_value"/>
        <attributeEditorField showLabel="1" index="7" name="channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer columnCount="1" groupBox="1" visibilityExpressionEnabled="0" showLabel="1" visibilityExpression="" name="Cross section">
        <attributeEditorField showLabel="1" index="8" name="cross_section_shape"/>
        <attributeEditorField showLabel="1" index="10" name="cross_section_height"/>
        <attributeEditorField showLabel="1" index="9" name="cross_section_width"/>
        <attributeEditorField showLabel="1" index="11" name="cross_section_table"/>
      </attributeEditorContainer>
    </attributeEditorContainer>
  </attributeEditorForm>
  <editable>
    <field editable="0" name="Cross section definition_height"/>
    <field editable="0" name="Cross section definition_shape"/>
    <field editable="0" name="Cross section definition_width"/>
    <field editable="1" name="ROWID"/>
    <field editable="1" name="bank_level"/>
    <field editable="1" name="channel_id"/>
    <field editable="1" name="code"/>
    <field editable="1" name="cross_section_height"/>
    <field editable="1" name="cross_section_shape"/>
    <field editable="1" name="cross_section_table"/>
    <field editable="1" name="cross_section_width"/>
    <field editable="1" name="definition_id"/>
    <field editable="1" name="fid"/>
    <field editable="1" name="friction_type"/>
    <field editable="1" name="friction_value"/>
    <field editable="1" name="id"/>
    <field editable="1" name="reference_level"/>
  </editable>
  <labelOnTop>
    <field labelOnTop="0" name="Cross section definition_height"/>
    <field labelOnTop="0" name="Cross section definition_shape"/>
    <field labelOnTop="0" name="Cross section definition_width"/>
    <field labelOnTop="0" name="ROWID"/>
    <field labelOnTop="0" name="bank_level"/>
    <field labelOnTop="0" name="channel_id"/>
    <field labelOnTop="0" name="code"/>
    <field labelOnTop="0" name="cross_section_height"/>
    <field labelOnTop="0" name="cross_section_shape"/>
    <field labelOnTop="0" name="cross_section_table"/>
    <field labelOnTop="0" name="cross_section_width"/>
    <field labelOnTop="0" name="definition_id"/>
    <field labelOnTop="0" name="fid"/>
    <field labelOnTop="0" name="friction_type"/>
    <field labelOnTop="0" name="friction_value"/>
    <field labelOnTop="0" name="id"/>
    <field labelOnTop="0" name="reference_level"/>
  </labelOnTop>
  <dataDefinedFieldProperties/>
  <widgets/>
  <previewExpression>"id"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
