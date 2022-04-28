<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis readOnly="0" styleCategories="LayerConfiguration|Symbology|Labeling|Fields|Forms" labelsEnabled="1" version="3.16.9-Hannover">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>0</Removable>
    <Searchable>1</Searchable>
  </flags>
  <renderer-v2 forceraster="0" symbollevels="0" enableorderby="0" type="singleSymbol">
    <symbols>
      <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="0" type="marker">
        <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
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
  <labeling type="rule-based">
    <rules key="{5c70c4dd-aa7a-4ad1-be6c-8af2c8cbe1ac}">
      <rule key="{33657286-5b8d-4c99-8515-3bd47e159ae9}" scalemaxdenom="5000" filter=" &quot;cross_section_shape&quot;  =  5  OR  &quot;cross_section_shape&quot;  =  6 ">
        <settings calloutType="simple">
          <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName=" max_height_width_label(  &quot;cross_section_table&quot; )" capitalization="0" namedStyle="Normalny" blendMode="0" fontWeight="50" fontSize="10" fontItalic="0" fontKerning="1" fontLetterSpacing="0" isExpression="1" textOrientation="horizontal" useSubstitutions="0" fontStrikeout="0" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" fontSizeUnit="Point" fontFamily="MS Shell Dlg 2" fontWordSpacing="0" fontUnderline="0" allowHtml="0" multilineHeight="1" textOpacity="1">
            <text-buffer bufferDraw="0" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferSizeUnits="MM" bufferJoinStyle="128" bufferSize="1" bufferNoFill="1" bufferColor="255,255,255,255"/>
            <text-mask maskType="0" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskOpacity="1" maskJoinStyle="128" maskEnabled="0" maskedSymbolLayers=""/>
            <background shapeBorderWidth="0" shapeRotationType="0" shapeBorderWidthUnit="MM" shapeRadiiUnit="MM" shapeRotation="0" shapeType="0" shapeSizeUnit="MM" shapeOffsetY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeSizeX="0" shapeJoinStyle="64" shapeOffsetX="0" shapeFillColor="255,255,255,255" shapeSizeType="0" shapeSizeY="0" shapeRadiiY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeBlendMode="0">
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="markerSymbol" type="marker">
                <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="125,139,143,255"/>
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
            <shadow shadowOffsetGlobal="1" shadowOffsetAngle="135" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowRadiusUnit="MM" shadowOffsetUnit="MM" shadowScale="100" shadowUnder="0" shadowOffsetDist="1" shadowRadius="1.5" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusAlphaOnly="0"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format wrapChar="" autoWrapLength="0" placeDirectionSymbol="0" rightDirectionSymbol=">" multilineAlign="3" useMaxLineLengthForAutoWrap="1" decimals="3" leftDirectionSymbol="&lt;" addDirectionSymbol="0" plussign="0" reverseDirectionSymbol="0" formatNumbers="0"/>
          <placement quadOffset="4" distUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorType="0" polygonPlacementFlags="2" placementFlags="10" distMapUnitScale="3x:0,0,0,0,0,0" dist="0" rotationAngle="0" lineAnchorPercent="0.5" repeatDistanceUnits="MM" geometryGeneratorType="PointGeometry" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" preserveRotation="1" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" placement="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetUnits="MM" repeatDistance="0" fitInPolygonOnly="0" centroidWhole="0" maxCurvedCharAngleIn="25" maxCurvedCharAngleOut="-25" xOffset="0" overrunDistance="0" layerType="PointGeometry" overrunDistanceUnit="MM" offsetType="0" yOffset="0" priority="5" centroidInside="0"/>
          <rendering minFeatureSize="0" obstacleType="1" upsidedownLabels="0" zIndex="0" displayAll="0" fontMinPixelSize="3" scaleVisibility="0" fontMaxPixelSize="10000" limitNumLabels="0" maxNumLabels="2000" scaleMin="0" drawLabels="1" labelPerPart="0" obstacleFactor="1" obstacle="1" mergeLines="0" fontLimitPixelSize="0" scaleMax="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
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
              <Option name="lineSymbol" type="QString" value="&lt;symbol alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot;>&lt;layer enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
      </rule>
      <rule key="{48c6139b-1985-4e81-a474-3b3dc2e15f6c}" scalemaxdenom="5000" filter="ELSE">
        <settings calloutType="simple">
          <text-style fontSizeMapUnitScale="3x:0,0,0,0,0,0" fieldName="'Height: ' +  to_string(  &quot;cross_section_height&quot; ) + '\n' + 'Width: ' +  to_string(  &quot;cross_section_width&quot; )" capitalization="0" namedStyle="Normalny" blendMode="0" fontWeight="50" fontSize="10" fontItalic="0" fontKerning="1" fontLetterSpacing="0" isExpression="1" textOrientation="horizontal" useSubstitutions="0" fontStrikeout="0" previewBkgrdColor="255,255,255,255" textColor="0,0,0,255" fontSizeUnit="Point" fontFamily="MS Shell Dlg 2" fontWordSpacing="0" fontUnderline="0" allowHtml="0" multilineHeight="1" textOpacity="1">
            <text-buffer bufferDraw="0" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferOpacity="1" bufferSizeUnits="MM" bufferJoinStyle="128" bufferSize="1" bufferNoFill="1" bufferColor="255,255,255,255"/>
            <text-mask maskType="0" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskSize="1.5" maskOpacity="1" maskJoinStyle="128" maskEnabled="0" maskedSymbolLayers=""/>
            <background shapeBorderWidth="0" shapeRotationType="0" shapeBorderWidthUnit="MM" shapeRadiiUnit="MM" shapeRotation="0" shapeType="0" shapeSizeUnit="MM" shapeOffsetY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeSizeX="0" shapeJoinStyle="64" shapeOffsetX="0" shapeFillColor="255,255,255,255" shapeSizeType="0" shapeSizeY="0" shapeRadiiY="0" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeSVGFile="" shapeRadiiX="0" shapeBorderColor="128,128,128,255" shapeDraw="0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetUnit="MM" shapeBlendMode="0">
              <symbol alpha="1" clip_to_extent="1" force_rhr="0" name="markerSymbol" type="marker">
                <layer enabled="1" locked="0" class="SimpleMarker" pass="0">
                  <prop k="angle" v="0"/>
                  <prop k="color" v="114,155,111,255"/>
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
            <shadow shadowOffsetGlobal="1" shadowOffsetAngle="135" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.7" shadowRadiusUnit="MM" shadowOffsetUnit="MM" shadowScale="100" shadowUnder="0" shadowOffsetDist="1" shadowRadius="1.5" shadowColor="0,0,0,255" shadowBlendMode="6" shadowRadiusAlphaOnly="0"/>
            <dd_properties>
              <Option type="Map">
                <Option name="name" type="QString" value=""/>
                <Option name="properties"/>
                <Option name="type" type="QString" value="collection"/>
              </Option>
            </dd_properties>
            <substitutions/>
          </text-style>
          <text-format wrapChar="" autoWrapLength="0" placeDirectionSymbol="0" rightDirectionSymbol=">" multilineAlign="3" useMaxLineLengthForAutoWrap="1" decimals="3" leftDirectionSymbol="&lt;" addDirectionSymbol="0" plussign="0" reverseDirectionSymbol="0" formatNumbers="0"/>
          <placement quadOffset="4" distUnits="MM" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" lineAnchorType="0" polygonPlacementFlags="2" placementFlags="10" distMapUnitScale="3x:0,0,0,0,0,0" dist="0" rotationAngle="0" lineAnchorPercent="0.5" repeatDistanceUnits="MM" geometryGeneratorType="PointGeometry" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGeneratorEnabled="0" preserveRotation="1" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" placement="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" offsetUnits="MM" repeatDistance="0" fitInPolygonOnly="0" centroidWhole="0" maxCurvedCharAngleIn="25" maxCurvedCharAngleOut="-25" xOffset="0" overrunDistance="0" layerType="PointGeometry" overrunDistanceUnit="MM" offsetType="0" yOffset="0" priority="5" centroidInside="0"/>
          <rendering minFeatureSize="0" obstacleType="1" upsidedownLabels="0" zIndex="0" displayAll="0" fontMinPixelSize="3" scaleVisibility="0" fontMaxPixelSize="10000" limitNumLabels="0" maxNumLabels="2000" scaleMin="0" drawLabels="1" labelPerPart="0" obstacleFactor="1" obstacle="1" mergeLines="0" fontLimitPixelSize="0" scaleMax="0"/>
          <dd_properties>
            <Option type="Map">
              <Option name="name" type="QString" value=""/>
              <Option name="properties"/>
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
              <Option name="lineSymbol" type="QString" value="&lt;symbol alpha=&quot;1&quot; clip_to_extent=&quot;1&quot; force_rhr=&quot;0&quot; name=&quot;symbol&quot; type=&quot;line&quot;>&lt;layer enabled=&quot;1&quot; locked=&quot;0&quot; class=&quot;SimpleLine&quot; pass=&quot;0&quot;>&lt;prop k=&quot;align_dash_pattern&quot; v=&quot;0&quot;/>&lt;prop k=&quot;capstyle&quot; v=&quot;square&quot;/>&lt;prop k=&quot;customdash&quot; v=&quot;5;2&quot;/>&lt;prop k=&quot;customdash_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;customdash_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;dash_pattern_offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;dash_pattern_offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;dash_pattern_offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;draw_inside_polygon&quot; v=&quot;0&quot;/>&lt;prop k=&quot;joinstyle&quot; v=&quot;bevel&quot;/>&lt;prop k=&quot;line_color&quot; v=&quot;60,60,60,255&quot;/>&lt;prop k=&quot;line_style&quot; v=&quot;solid&quot;/>&lt;prop k=&quot;line_width&quot; v=&quot;0.3&quot;/>&lt;prop k=&quot;line_width_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;offset&quot; v=&quot;0&quot;/>&lt;prop k=&quot;offset_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;prop k=&quot;offset_unit&quot; v=&quot;MM&quot;/>&lt;prop k=&quot;ring_filter&quot; v=&quot;0&quot;/>&lt;prop k=&quot;tweak_dash_pattern_on_corners&quot; v=&quot;0&quot;/>&lt;prop k=&quot;use_custom_dash&quot; v=&quot;0&quot;/>&lt;prop k=&quot;width_map_unit_scale&quot; v=&quot;3x:0,0,0,0,0,0&quot;/>&lt;data_defined_properties>&lt;Option type=&quot;Map&quot;>&lt;Option name=&quot;name&quot; type=&quot;QString&quot; value=&quot;&quot;/>&lt;Option name=&quot;properties&quot;/>&lt;Option name=&quot;type&quot; type=&quot;QString&quot; value=&quot;collection&quot;/>&lt;/Option>&lt;/data_defined_properties>&lt;/layer>&lt;/symbol>"/>
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
      </rule>
    </rules>
  </labeling>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <fieldConfiguration>
    <field configurationFlags="None" name="fid">
      <editWidget type="TextEdit">
        <config>
          <Option/>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="id">
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
    <field configurationFlags="None" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option name="IsMultiline" type="bool" value="false"/>
            <Option name="UseHtml" type="bool" value="false"/>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="reference_level">
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
    <field configurationFlags="None" name="friction_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Chezy" type="int" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="Manning" type="int" value="2"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="friction_value">
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
    <field configurationFlags="None" name="bank_level">
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
    <field configurationFlags="None" name="channel_id">
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
    <field configurationFlags="None" name="cross_section_shape">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option name="map" type="List">
              <Option type="Map">
                <Option name="Rectangle" type="int" value="1"/>
              </Option>
              <Option type="Map">
                <Option name="Circle" type="int" value="2"/>
              </Option>
              <Option type="Map">
                <Option name="Egg" type="int" value="3"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated rectangle" type="int" value="5"/>
              </Option>
              <Option type="Map">
                <Option name="Tabulated trapezium" type="int" value="6"/>
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="None" name="cross_section_width">
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
    <field configurationFlags="None" name="cross_section_height">
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
    <field configurationFlags="None" name="cross_section_table">
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
    <constraint exp_strength="0" field="fid" notnull_strength="1" constraints="3" unique_strength="1"/>
    <constraint exp_strength="0" field="id" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="code" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="reference_level" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="friction_type" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="friction_value" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="bank_level" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="channel_id" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="cross_section_shape" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="cross_section_width" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="cross_section_height" notnull_strength="0" constraints="0" unique_strength="0"/>
    <constraint exp_strength="0" field="cross_section_table" notnull_strength="0" constraints="0" unique_strength="0"/>
  </constraints>
  <constraintExpressions>
    <constraint desc="" exp="" field="fid"/>
    <constraint desc="" exp="" field="id"/>
    <constraint desc="" exp="" field="code"/>
    <constraint desc="" exp="" field="reference_level"/>
    <constraint desc="" exp="" field="friction_type"/>
    <constraint desc="" exp="" field="friction_value"/>
    <constraint desc="" exp="" field="bank_level"/>
    <constraint desc="" exp="" field="channel_id"/>
    <constraint desc="" exp="" field="cross_section_shape"/>
    <constraint desc="" exp="" field="cross_section_width"/>
    <constraint desc="" exp="" field="cross_section_height"/>
    <constraint desc="" exp="" field="cross_section_table"/>
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
    <attributeEditorContainer showLabel="1" groupBox="0" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" name="Cross section location view">
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" name="General">
        <attributeEditorField showLabel="1" index="1" name="id"/>
        <attributeEditorField showLabel="1" index="2" name="code"/>
        <attributeEditorField showLabel="1" index="3" name="reference_level"/>
        <attributeEditorField showLabel="1" index="6" name="bank_level"/>
        <attributeEditorField showLabel="1" index="4" name="friction_type"/>
        <attributeEditorField showLabel="1" index="5" name="friction_value"/>
        <attributeEditorField showLabel="1" index="7" name="channel_id"/>
      </attributeEditorContainer>
      <attributeEditorContainer showLabel="1" groupBox="1" visibilityExpressionEnabled="0" visibilityExpression="" columnCount="1" name="Cross section">
        <attributeEditorField showLabel="1" index="8" name="cross_section_shape"/>
        <attributeEditorField showLabel="1" index="10" name="cross_section_height"/>
        <attributeEditorField showLabel="1" index="9" name="cross_section_width"/>
        <attributeEditorField showLabel="1" index="11" name="cross_section_table"/>
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
  <previewExpression>"fid"</previewExpression>
  <layerGeometryType>0</layerGeometryType>
</qgis>
