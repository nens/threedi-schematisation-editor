<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" maxScale="0" version="3.16.9-Hannover" minScale="1e+08" hasScaleBasedVisibilityFlag="0">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal enabled="0" mode="0" fetchMode="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property key="WMSBackgroundLayer" value="false"/>
    <property key="WMSPublishDataSourceUrl" value="false"/>
    <property key="embeddedWidgets/count" value="0"/>
    <property key="identify/format" value="Value"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="0.015" opacity="1" alphaBand="-1" band="1" classificationMax="9999">
      <rasterTransparency/>
      <minMaxOrigin>
        <limits>MinMax</limits>
        <extent>WholeRaster</extent>
        <statAccuracy>Estimated</statAccuracy>
        <cumulativeCutLower>0.02</cumulativeCutLower>
        <cumulativeCutUpper>0.98</cumulativeCutUpper>
        <stdDevFactor>2</stdDevFactor>
      </minMaxOrigin>
      <rastershader>
        <colorrampshader minimumValue="0.015" classificationMode="2" maximumValue="9999" clip="0" labelPrecision="4" colorRampType="INTERPOLATED">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="241,238,246,255"/>
            <prop k="color2" v="152,0,67,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.25;215,181,216,255:0.5;223,101,176,255:0.75;221,28,119,255"/>
          </colorramp>
          <item label="0,0150" color="#f1eef6" alpha="255" value="0.0149999996647239"/>
          <item label="1111,0133" color="#e6d5e9" alpha="255" value="1111.0133333330352"/>
          <item label="2222,0117" color="#dabcdc" alpha="255" value="2222.0116666664057"/>
          <item label="3333,0100" color="#da9acb" alpha="255" value="3333.0099999997765"/>
          <item label="4444,0083" color="#de77b9" alpha="255" value="4444.008333333147"/>
          <item label="5555,0067" color="#df55a3" alpha="255" value="5555.006666666517"/>
          <item label="6666,0050" color="#de348a" alpha="255" value="6666.004999999888"/>
          <item label="7777,0033" color="#d61871" alpha="255" value="7777.0033333332585"/>
          <item label="8888,0017" color="#b70c5a" alpha="255" value="8888.001666666629"/>
          <item label="9999,0000" color="#980043" alpha="255" value="9999"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast gamma="1" contrast="0" brightness="0"/>
    <huesaturation colorizeRed="255" colorizeOn="0" saturation="0" colorizeGreen="128" colorizeStrength="100" grayscaleMode="0" colorizeBlue="128"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
