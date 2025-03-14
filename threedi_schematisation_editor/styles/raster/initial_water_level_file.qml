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
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="-10" opacity="1" alphaBand="-1" band="1" classificationMax="0">
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
        <colorrampshader minimumValue="-10" classificationMode="2" maximumValue="0" clip="0" labelPrecision="4" colorRampType="INTERPOLATED">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="247,251,255,255"/>
            <prop k="color2" v="8,48,107,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.13;222,235,247,255:0.26;198,219,239,255:0.39;158,202,225,255:0.52;107,174,214,255:0.65;66,146,198,255:0.78;33,113,181,255:0.9;8,81,156,255"/>
          </colorramp>
          <item label="-10,0000" color="#f7fbff" alpha="255" value="-10"/>
          <item label="-8,8889" color="#e2eef9" alpha="255" value="-8.88888888888889"/>
          <item label="-7,7778" color="#cde0f2" alpha="255" value="-7.777777777777778"/>
          <item label="-6,6667" color="#b0d2e8" alpha="255" value="-6.666666666666666"/>
          <item label="-5,5556" color="#89bfdd" alpha="255" value="-5.555555555555555"/>
          <item label="-4,4444" color="#60a6d2" alpha="255" value="-4.444444444444445"/>
          <item label="-3,3333" color="#3e8ec4" alpha="255" value="-3.333333333333333"/>
          <item label="-2,2222" color="#2172b6" alpha="255" value="-2.222222222222221"/>
          <item label="-1,1111" color="#0a549e" alpha="255" value="-1.11111111111111"/>
          <item label="0,0000" color="#08306b" alpha="255" value="0"/>
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
