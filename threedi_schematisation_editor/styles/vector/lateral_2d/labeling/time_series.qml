<?xml version='1.0' encoding='utf-8'?>
<qgis><labeling type="simple">
    <settings calloutType="simple">
      <text-style fontWordSpacing="0" textOrientation="horizontal" fieldName="right(represent_value(type), length(represent_value(type)) - 3) || ' lateral\n' ||&#13;&#10;'min: '||&#13;&#10;format_number(&#13;&#10;&#09;array_first(&#13;&#10;&#09;&#09;array_sort(&#13;&#10;&#09;&#09;&#09;array_foreach(&#13;&#10;&#09;&#09;&#09;&#09;string_to_array(timeseries,  '\n' ),&#13;&#10;&#09;&#09;&#09;&#09;to_real(&#13;&#10;&#09;&#09;&#09;&#09;&#09;array_last(&#13;&#10;&#09;&#09;&#09;&#09;&#09;&#09;string_to_array(@element, ',')&#13;&#10;&#09;&#09;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;),&#13;&#10;&#09;2&#13;&#10;) || ' ' || units&#13;&#10;|| '\nmax: ' ||&#13;&#10;format_number(&#13;&#10;&#09;array_last(&#13;&#10;&#09;&#09;array_sort(&#13;&#10;&#09;&#09;&#09;array_foreach(&#13;&#10;&#09;&#09;&#09;&#09;string_to_array(timeseries,  '\n' ),&#13;&#10;&#09;&#09;&#09;&#09;to_real(&#13;&#10;&#09;&#09;&#09;&#09;&#09;array_last(&#13;&#10;&#09;&#09;&#09;&#09;&#09;&#09;string_to_array(@element, ',')&#13;&#10;&#09;&#09;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;&#09;)&#13;&#10;&#09;&#09;)&#13;&#10;&#09;),&#13;&#10;&#09;2&#13;&#10;) || ' ' || units&#13;&#10;" fontKerning="1" fontStrikeout="0" fontItalic="0" fontSize="8" previewBkgrdColor="255,255,255,255" fontLetterSpacing="0" capitalization="0" fontWeight="50" isExpression="1" legendString="Aa" allowHtml="0" namedStyle="Regular" fontSizeMapUnitScale="3x:0,0,0,0,0,0" multilineHeightUnit="Percentage" forcedItalic="0" useSubstitutions="0" blendMode="0" fontUnderline="0" textColor="0,0,0,255" fontFamily="MS Gothic" multilineHeight="1" textOpacity="1" fontSizeUnit="Point" forcedBold="0">
        <families />
        <text-buffer bufferSizeUnits="MM" bufferColor="255,255,255,255" bufferBlendMode="0" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferJoinStyle="128" bufferDraw="1" bufferNoFill="1" bufferOpacity="1" bufferSize="0.69999999999999996" />
        <text-mask maskSize="0" maskJoinStyle="128" maskOpacity="1" maskedSymbolLayers="" maskSizeUnits="MM" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskType="0" maskEnabled="0" />
        <background shapeSizeUnit="MM" shapeRotationType="0" shapeRadiiUnit="MM" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeSizeY="0" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeOpacity="1" shapeBlendMode="0" shapeOffsetUnit="MM" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeOffsetX="0" shapeFillColor="255,255,255,255" shapeSizeX="0" shapeBorderWidth="0" shapeType="0" shapeSVGFile="" shapeSizeType="0" shapeJoinStyle="64" shapeBorderWidthUnit="MM" shapeRotation="0" shapeOffsetY="0" shapeRadiiY="0" shapeBorderColor="128,128,128,255" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeDraw="0" shapeRadiiX="0">
          <symbol clip_to_extent="1" is_animated="0" name="markerSymbol" alpha="1" frame_rate="10" type="marker" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString" />
                <Option name="properties" />
                <Option value="collection" name="type" type="QString" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleMarker" id="" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="0" name="angle" type="QString" />
                <Option value="square" name="cap_style" type="QString" />
                <Option value="125,139,143,255" name="color" type="QString" />
                <Option value="1" name="horizontal_anchor_point" type="QString" />
                <Option value="bevel" name="joinstyle" type="QString" />
                <Option value="circle" name="name" type="QString" />
                <Option value="0,0" name="offset" type="QString" />
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString" />
                <Option value="MM" name="offset_unit" type="QString" />
                <Option value="35,35,35,255" name="outline_color" type="QString" />
                <Option value="solid" name="outline_style" type="QString" />
                <Option value="0" name="outline_width" type="QString" />
                <Option value="3x:0,0,0,0,0,0" name="outline_width_map_unit_scale" type="QString" />
                <Option value="MM" name="outline_width_unit" type="QString" />
                <Option value="diameter" name="scale_method" type="QString" />
                <Option value="2" name="size" type="QString" />
                <Option value="3x:0,0,0,0,0,0" name="size_map_unit_scale" type="QString" />
                <Option value="MM" name="size_unit" type="QString" />
                <Option value="1" name="vertical_anchor_point" type="QString" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString" />
                  <Option name="properties" />
                  <Option value="collection" name="type" type="QString" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol clip_to_extent="1" is_animated="0" name="fillSymbol" alpha="1" frame_rate="10" type="fill" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option value="" name="name" type="QString" />
                <Option name="properties" />
                <Option value="collection" name="type" type="QString" />
              </Option>
            </data_defined_properties>
            <layer class="SimpleFill" id="" enabled="1" locked="0" pass="0">
              <Option type="Map">
                <Option value="3x:0,0,0,0,0,0" name="border_width_map_unit_scale" type="QString" />
                <Option value="255,255,255,255" name="color" type="QString" />
                <Option value="bevel" name="joinstyle" type="QString" />
                <Option value="0,0" name="offset" type="QString" />
                <Option value="3x:0,0,0,0,0,0" name="offset_map_unit_scale" type="QString" />
                <Option value="MM" name="offset_unit" type="QString" />
                <Option value="128,128,128,255" name="outline_color" type="QString" />
                <Option value="no" name="outline_style" type="QString" />
                <Option value="0" name="outline_width" type="QString" />
                <Option value="MM" name="outline_width_unit" type="QString" />
                <Option value="solid" name="style" type="QString" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option value="" name="name" type="QString" />
                  <Option name="properties" />
                  <Option value="collection" name="type" type="QString" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowBlendMode="6" shadowOffsetAngle="135" shadowOffsetDist="1" shadowRadiusUnit="MM" shadowUnder="0" shadowColor="0,0,0,255" shadowRadiusAlphaOnly="0" shadowRadius="1.5" shadowDraw="0" shadowOffsetGlobal="1" shadowScale="100" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowOpacity="0.69999999999999996" shadowOffsetUnit="MM" />
        <dd_properties>
          <Option type="Map">
            <Option value="" name="name" type="QString" />
            <Option name="properties" />
            <Option value="collection" name="type" type="QString" />
          </Option>
        </dd_properties>
        <substitutions />
      </text-style>
      <text-format rightDirectionSymbol="&gt;" wrapChar="" autoWrapLength="0" placeDirectionSymbol="0" multilineAlign="0" reverseDirectionSymbol="0" addDirectionSymbol="0" leftDirectionSymbol="&lt;" plussign="0" formatNumbers="0" decimals="3" useMaxLineLengthForAutoWrap="1" />
      <placement maxCurvedCharAngleIn="25" yOffset="0" distUnits="MM" offsetType="0" lineAnchorTextPoint="FollowPlacement" overrunDistance="0" allowDegraded="0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" geometryGenerator="" placementFlags="10" polygonPlacementFlags="2" geometryGeneratorEnabled="0" overrunDistanceUnit="MM" preserveRotation="1" placement="6" overlapHandling="PreventOverlap" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" centroidInside="0" maxCurvedCharAngleOut="-25" repeatDistanceUnits="MM" geometryGeneratorType="PointGeometry" distMapUnitScale="3x:0,0,0,0,0,0" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" fitInPolygonOnly="0" rotationAngle="0" quadOffset="4" layerType="PointGeometry" rotationUnit="AngleDegrees" centroidWhole="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" xOffset="0" lineAnchorPercent="0.5" repeatDistance="0" lineAnchorClipping="0" lineAnchorType="0" offsetUnits="MM" dist="0" priority="5" />
      <rendering obstacleFactor="1" obstacle="1" zIndex="0" unplacedVisibility="0" labelPerPart="0" upsidedownLabels="0" limitNumLabels="0" scaleVisibility="0" scaleMax="0" fontMaxPixelSize="10000" maxNumLabels="2000" minFeatureSize="0" obstacleType="0" fontMinPixelSize="3" mergeLines="0" drawLabels="1" fontLimitPixelSize="0" scaleMin="0" />
      <dd_properties>
        <Option type="Map">
          <Option value="" name="name" type="QString" />
          <Option name="properties" />
          <Option value="collection" name="type" type="QString" />
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option value="pole_of_inaccessibility" name="anchorPoint" type="QString" />
          <Option value="0" name="blendMode" type="int" />
          <Option name="ddProperties" type="Map">
            <Option value="" name="name" type="QString" />
            <Option name="properties" />
            <Option value="collection" name="type" type="QString" />
          </Option>
          <Option value="false" name="drawToAllParts" type="bool" />
          <Option value="0" name="enabled" type="QString" />
          <Option value="point_on_exterior" name="labelAnchorPoint" type="QString" />
          <Option value="&lt;symbol clip_to_extent=&quot;1&quot; is_animated=&quot;0&quot; name=&quot;symbol&quot; alpha=&quot;1&quot; frame_rate=&quot;10&quot; type=&quot;line&quot; force_rhr=&quot;0&quot;&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;layer class=&quot;SimpleLine&quot; id=&quot;{b06dff41-25f1-465f-9e2d-cddac4e05f7d}&quot; enabled=&quot;1&quot; locked=&quot;0&quot; pass=&quot;0&quot;&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option value=&quot;0&quot; name=&quot;align_dash_pattern&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;square&quot; name=&quot;capstyle&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;5;2&quot; name=&quot;customdash&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;customdash_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;customdash_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;dash_pattern_offset&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;dash_pattern_offset_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;dash_pattern_offset_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;draw_inside_polygon&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;bevel&quot; name=&quot;joinstyle&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;60,60,60,255&quot; name=&quot;line_color&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;solid&quot; name=&quot;line_style&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0.3&quot; name=&quot;line_width&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;line_width_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;offset&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;offset_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;offset_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;ring_filter&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;trim_distance_end&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_end_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_end_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;trim_distance_start&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;trim_distance_start_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;MM&quot; name=&quot;trim_distance_start_unit&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;tweak_dash_pattern_on_corners&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;0&quot; name=&quot;use_custom_dash&quot; type=&quot;QString&quot;/&gt;&lt;Option value=&quot;3x:0,0,0,0,0,0&quot; name=&quot;width_map_unit_scale&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option value=&quot;&quot; name=&quot;name&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option value=&quot;collection&quot; name=&quot;type&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;/layer&gt;&lt;/symbol&gt;" name="lineSymbol" type="QString" />
          <Option value="0" name="minLength" type="double" />
          <Option value="3x:0,0,0,0,0,0" name="minLengthMapUnitScale" type="QString" />
          <Option value="MM" name="minLengthUnit" type="QString" />
          <Option value="0" name="offsetFromAnchor" type="double" />
          <Option value="3x:0,0,0,0,0,0" name="offsetFromAnchorMapUnitScale" type="QString" />
          <Option value="MM" name="offsetFromAnchorUnit" type="QString" />
          <Option value="0" name="offsetFromLabel" type="double" />
          <Option value="3x:0,0,0,0,0,0" name="offsetFromLabelMapUnitScale" type="QString" />
          <Option value="MM" name="offsetFromLabelUnit" type="QString" />
        </Option>
      </callout>
    </settings>
  </labeling>
  </qgis>