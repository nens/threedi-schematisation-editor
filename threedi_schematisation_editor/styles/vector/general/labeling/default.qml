<?xml version='1.0' encoding='utf-8'?>
<qgis><labeling type="simple">
    <settings calloutType="simple">
      <text-style fontKerning="1" useSubstitutions="0" fontFamily="MS Shell Dlg 2" allowHtml="0" forcedItalic="0" blendMode="0" fontWeight="75" fieldName="with_variable(&#13;&#10;&#09;'nr_intersections',&#13;&#10;&#09;array_length(overlay_equals(layer:=@layer, expression:= geom_to_wkt(@geometry))),&#13;&#10;&#09;if(@nr_intersections&gt;0,@nr_intersections + 1,NULL)&#13;&#10;)" textOrientation="horizontal" previewBkgrdColor="255,255,255,255" fontItalic="0" multilineHeightUnit="Percentage" fontSize="10" fontStrikeout="0" textColor="60,60,60,255" fontSizeUnit="Point" multilineHeight="1" fontUnderline="0" namedStyle="Bold" forcedBold="0" isExpression="1" legendString="Aa" capitalization="0" textOpacity="1" fontLetterSpacing="0" fontWordSpacing="0" fontSizeMapUnitScale="3x:0,0,0,0,0,0">
        <families />
        <text-buffer bufferBlendMode="0" bufferDraw="1" bufferSizeUnits="MM" bufferOpacity="1" bufferSizeMapUnitScale="3x:0,0,0,0,0,0" bufferColor="255,255,255,255" bufferNoFill="0" bufferSize="0.69999999999999996" bufferJoinStyle="128" />
        <text-mask maskSizeUnits="MM" maskedSymbolLayers="" maskSize="0" maskType="0" maskOpacity="1" maskSizeMapUnitScale="3x:0,0,0,0,0,0" maskJoinStyle="128" maskEnabled="0" />
        <background shapeRotationType="0" shapeBorderWidth="0" shapeType="5" shapeOffsetY="0" shapeSizeUnit="MM" shapeOffsetMapUnitScale="3x:0,0,0,0,0,0" shapeRadiiY="0" shapeBorderWidthMapUnitScale="3x:0,0,0,0,0,0" shapeSizeMapUnitScale="3x:0,0,0,0,0,0" shapeBorderWidthUnit="MM" shapeSizeType="0" shapeSizeY="0" shapeDraw="1" shapeFillColor="255,255,255,255" shapeRadiiMapUnitScale="3x:0,0,0,0,0,0" shapeBlendMode="0" shapeJoinStyle="64" shapeSVGFile="" shapeOffsetX="0" shapeSizeX="0" shapeRadiiX="0" shapeOpacity="1" shapeBorderColor="128,128,128,255" shapeRotation="0" shapeOffsetUnit="MM" shapeRadiiUnit="MM">
          <symbol frame_rate="10" name="markerSymbol" clip_to_extent="1" is_animated="0" type="marker" alpha="1" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString" />
                <Option name="properties" />
                <Option name="type" value="collection" type="QString" />
              </Option>
            </data_defined_properties>
            <layer locked="0" id="" pass="0" class="SimpleMarker" enabled="1">
              <Option type="Map">
                <Option name="angle" value="0" type="QString" />
                <Option name="cap_style" value="square" type="QString" />
                <Option name="color" value="255,255,255,255" type="QString" />
                <Option name="horizontal_anchor_point" value="1" type="QString" />
                <Option name="joinstyle" value="bevel" type="QString" />
                <Option name="name" value="circle" type="QString" />
                <Option name="offset" value="0,0" type="QString" />
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString" />
                <Option name="offset_unit" value="MM" type="QString" />
                <Option name="outline_color" value="60,60,60,255" type="QString" />
                <Option name="outline_style" value="solid" type="QString" />
                <Option name="outline_width" value="0.4" type="QString" />
                <Option name="outline_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString" />
                <Option name="outline_width_unit" value="MM" type="QString" />
                <Option name="scale_method" value="diameter" type="QString" />
                <Option name="size" value="4" type="QString" />
                <Option name="size_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString" />
                <Option name="size_unit" value="MM" type="QString" />
                <Option name="vertical_anchor_point" value="1" type="QString" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString" />
                  <Option name="properties" />
                  <Option name="type" value="collection" type="QString" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
          <symbol frame_rate="10" name="fillSymbol" clip_to_extent="1" is_animated="0" type="fill" alpha="1" force_rhr="0">
            <data_defined_properties>
              <Option type="Map">
                <Option name="name" value="" type="QString" />
                <Option name="properties" />
                <Option name="type" value="collection" type="QString" />
              </Option>
            </data_defined_properties>
            <layer locked="0" id="" pass="0" class="SimpleFill" enabled="1">
              <Option type="Map">
                <Option name="border_width_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString" />
                <Option name="color" value="255,255,255,255" type="QString" />
                <Option name="joinstyle" value="bevel" type="QString" />
                <Option name="offset" value="0,0" type="QString" />
                <Option name="offset_map_unit_scale" value="3x:0,0,0,0,0,0" type="QString" />
                <Option name="offset_unit" value="MM" type="QString" />
                <Option name="outline_color" value="128,128,128,255" type="QString" />
                <Option name="outline_style" value="no" type="QString" />
                <Option name="outline_width" value="0" type="QString" />
                <Option name="outline_width_unit" value="MM" type="QString" />
                <Option name="style" value="solid" type="QString" />
              </Option>
              <data_defined_properties>
                <Option type="Map">
                  <Option name="name" value="" type="QString" />
                  <Option name="properties" />
                  <Option name="type" value="collection" type="QString" />
                </Option>
              </data_defined_properties>
            </layer>
          </symbol>
        </background>
        <shadow shadowOffsetDist="1" shadowRadius="1.5" shadowBlendMode="6" shadowUnder="0" shadowOffsetUnit="MM" shadowOffsetGlobal="1" shadowRadiusAlphaOnly="0" shadowOpacity="0.69999999999999996" shadowDraw="0" shadowOffsetMapUnitScale="3x:0,0,0,0,0,0" shadowColor="0,0,0,255" shadowRadiusMapUnitScale="3x:0,0,0,0,0,0" shadowScale="100" shadowOffsetAngle="135" shadowRadiusUnit="MM" />
        <dd_properties>
          <Option type="Map">
            <Option name="name" value="" type="QString" />
            <Option name="properties" />
            <Option name="type" value="collection" type="QString" />
          </Option>
        </dd_properties>
        <substitutions />
      </text-style>
      <text-format multilineAlign="0" useMaxLineLengthForAutoWrap="1" wrapChar="" autoWrapLength="0" rightDirectionSymbol="&gt;" addDirectionSymbol="0" plussign="0" formatNumbers="0" leftDirectionSymbol="&lt;" reverseDirectionSymbol="0" decimals="3" placeDirectionSymbol="0" />
      <placement preserveRotation="0" lineAnchorTextPoint="CenterOfText" overrunDistance="0" predefinedPositionOrder="TR,TL,BR,BL,R,L,TSR,BSR" distMapUnitScale="3x:0,0,0,0,0,0" labelOffsetMapUnitScale="3x:0,0,0,0,0,0" lineAnchorPercent="0.5" geometryGenerator="centroid($geometry)" layerType="LineGeometry" overrunDistanceUnit="MM" fitInPolygonOnly="0" maxCurvedCharAngleOut="-25" repeatDistanceMapUnitScale="3x:0,0,0,0,0,0" distUnits="MM" priority="5" maxCurvedCharAngleIn="25" overrunDistanceMapUnitScale="3x:0,0,0,0,0,0" polygonPlacementFlags="2" offsetType="0" dist="0" repeatDistanceUnits="MM" geometryGeneratorType="PointGeometry" offsetUnits="MM" geometryGeneratorEnabled="1" xOffset="4" centroidInside="0" placement="1" lineAnchorType="0" overlapHandling="AllowOverlapIfRequired" allowDegraded="1" quadOffset="2" repeatDistance="0" rotationUnit="AngleDegrees" centroidWhole="0" rotationAngle="0" lineAnchorClipping="0" yOffset="-4" placementFlags="2" />
      <rendering limitNumLabels="0" zIndex="0" upsidedownLabels="0" fontMaxPixelSize="10000" unplacedVisibility="0" fontMinPixelSize="3" labelPerPart="0" obstacle="1" fontLimitPixelSize="0" scaleVisibility="1" obstacleType="0" maxNumLabels="2000" minFeatureSize="0" drawLabels="1" scaleMax="2500" scaleMin="1" mergeLines="0" obstacleFactor="1" />
      <dd_properties>
        <Option type="Map">
          <Option name="name" value="" type="QString" />
          <Option name="properties" type="Map">
            <Option name="Hali" type="Map">
              <Option name="active" value="true" type="bool" />
              <Option name="expression" value="'Left'" type="QString" />
              <Option name="type" value="3" type="int" />
            </Option>
            <Option name="LabelRotation" type="Map">
              <Option name="active" value="false" type="bool" />
              <Option name="type" value="1" type="int" />
              <Option name="val" value="" type="QString" />
            </Option>
            <Option name="PositionX" type="Map">
              <Option name="active" value="false" type="bool" />
              <Option name="type" value="1" type="int" />
              <Option name="val" value="" type="QString" />
            </Option>
            <Option name="PositionY" type="Map">
              <Option name="active" value="false" type="bool" />
              <Option name="type" value="1" type="int" />
              <Option name="val" value="" type="QString" />
            </Option>
            <Option name="Vali" type="Map">
              <Option name="active" value="true" type="bool" />
              <Option name="expression" value="'Top'" type="QString" />
              <Option name="type" value="3" type="int" />
            </Option>
          </Option>
          <Option name="type" value="collection" type="QString" />
        </Option>
      </dd_properties>
      <callout type="simple">
        <Option type="Map">
          <Option name="anchorPoint" value="pole_of_inaccessibility" type="QString" />
          <Option name="blendMode" value="0" type="int" />
          <Option name="ddProperties" type="Map">
            <Option name="name" value="" type="QString" />
            <Option name="properties" />
            <Option name="type" value="collection" type="QString" />
          </Option>
          <Option name="drawToAllParts" value="false" type="bool" />
          <Option name="enabled" value="1" type="QString" />
          <Option name="labelAnchorPoint" value="centroid" type="QString" />
          <Option name="lineSymbol" value="&lt;symbol frame_rate=&quot;10&quot; name=&quot;symbol&quot; clip_to_extent=&quot;1&quot; is_animated=&quot;0&quot; type=&quot;line&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;layer locked=&quot;0&quot; id=&quot;{8cdd11df-b27b-4857-a53c-33d38400955f}&quot; pass=&quot;0&quot; class=&quot;ArrowLine&quot; enabled=&quot;1&quot;&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;arrow_start_width&quot; value=&quot;4&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_start_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_start_width_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_type&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_width&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;arrow_width_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_length&quot; value=&quot;1.5&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_length_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_length_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_thickness&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_thickness_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_thickness_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;head_type&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;is_curved&quot; value=&quot;1&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;is_repeated&quot; value=&quot;1&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;ring_filter&quot; value=&quot;0&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;symbol frame_rate=&quot;10&quot; name=&quot;@symbol@0&quot; clip_to_extent=&quot;1&quot; is_animated=&quot;0&quot; type=&quot;fill&quot; alpha=&quot;1&quot; force_rhr=&quot;0&quot;&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;layer locked=&quot;0&quot; id=&quot;{029996ba-cce6-427d-9339-07d4440170fc}&quot; pass=&quot;0&quot; class=&quot;SimpleFill&quot; enabled=&quot;1&quot;&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;border_width_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;joinstyle&quot; value=&quot;bevel&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset&quot; value=&quot;0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset_map_unit_scale&quot; value=&quot;3x:0,0,0,0,0,0&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;offset_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;outline_color&quot; value=&quot;60,60,60,255&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;outline_style&quot; value=&quot;no&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;outline_width&quot; value=&quot;0.3&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;outline_width_unit&quot; value=&quot;MM&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;style&quot; value=&quot;solid&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;data_defined_properties&gt;&lt;Option type=&quot;Map&quot;&gt;&lt;Option name=&quot;name&quot; value=&quot;&quot; type=&quot;QString&quot;/&gt;&lt;Option name=&quot;properties&quot;/&gt;&lt;Option name=&quot;type&quot; value=&quot;collection&quot; type=&quot;QString&quot;/&gt;&lt;/Option&gt;&lt;/data_defined_properties&gt;&lt;/layer&gt;&lt;/symbol&gt;&lt;/layer&gt;&lt;/symbol&gt;" type="QString" />
          <Option name="minLength" value="0" type="double" />
          <Option name="minLengthMapUnitScale" value="3x:0,0,0,0,0,0" type="QString" />
          <Option name="minLengthUnit" value="MM" type="QString" />
          <Option name="offsetFromAnchor" value="0" type="double" />
          <Option name="offsetFromAnchorMapUnitScale" value="3x:0,0,0,0,0,0" type="QString" />
          <Option name="offsetFromAnchorUnit" value="MM" type="QString" />
          <Option name="offsetFromLabel" value="0" type="double" />
          <Option name="offsetFromLabelMapUnitScale" value="3x:0,0,0,0,0,0" type="QString" />
          <Option name="offsetFromLabelUnit" value="MM" type="QString" />
        </Option>
      </callout>
    </settings>
  </labeling>
  </qgis>