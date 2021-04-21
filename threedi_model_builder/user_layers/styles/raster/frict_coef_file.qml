<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis styleCategories="AllStyleCategories" hasScaleBasedVisibilityFlag="0" maxScale="0" version="3.16.4-Hannover" minScale="1e+08">
  <flags>
    <Identifiable>1</Identifiable>
    <Removable>1</Removable>
    <Searchable>1</Searchable>
  </flags>
  <temporal mode="0" fetchMode="0" enabled="0">
    <fixedRange>
      <start></start>
      <end></end>
    </fixedRange>
  </temporal>
  <customproperties>
    <property value="false" key="WMSBackgroundLayer"/>
    <property value="false" key="WMSPublishDataSourceUrl"/>
    <property value="0" key="embeddedWidgets/count"/>
    <property value="Value" key="identify/format"/>
  </customproperties>
  <pipe>
    <provider>
      <resampling maxOversampling="2" enabled="false" zoomedOutResamplingMethod="nearestNeighbour" zoomedInResamplingMethod="nearestNeighbour"/>
    </provider>
    <rasterrenderer band="1" alphaBand="-1" classificationMin="0.013" classificationMax="0.058" opacity="1" nodataColor="" type="singlebandpseudocolor">
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
        <colorrampshader clip="0" colorRampType="INTERPOLATED" classificationMode="1" maximumValue="0.058" minimumValue="0.013" labelPrecision="4">
          <colorramp name="[source]" type="gradient">
            <prop k="color1" v="68,1,84,255"/>
            <prop k="color2" v="253,231,37,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.117647;71,42,122,255:0.215686;63,72,137,255:0.313725;51,99,141,255:0.411765;41,123,142,255:0.509804;32,146,140,255:0.607843;36,170,131,255:0.705882;70,192,111,255:0.803922;124,210,80,255:0.901961;189,223,38,255"/>
          </colorramp>
          <item label="0.0130" value="0.013" color="#440154" alpha="255"/>
          <item label="0.0183" value="0.018294115" color="#472a7a" alpha="255"/>
          <item label="0.0227" value="0.02270587" color="#3f4889" alpha="255"/>
          <item label="0.0271" value="0.027117625" color="#33638d" alpha="255"/>
          <item label="0.0315" value="0.031529425" color="#297b8e" alpha="255"/>
          <item label="0.0359" value="0.03594118" color="#20928c" alpha="255"/>
          <item label="0.0404" value="0.040352935" color="#24aa83" alpha="255"/>
          <item label="0.0448" value="0.04476469" color="#46c06f" alpha="255"/>
          <item label="0.0492" value="0.04917649" color="#7cd250" alpha="255"/>
          <item label="0.0536" value="0.053588245" color="#bddf26" alpha="255"/>
          <item label="0.0580" value="0.058" color="#fde725" alpha="255"/>
        </colorrampshader>
      </rastershader>
    </rasterrenderer>
    <brightnesscontrast contrast="0" brightness="0" gamma="1"/>
    <huesaturation colorizeBlue="128" grayscaleMode="0" saturation="0" colorizeGreen="128" colorizeOn="0" colorizeRed="255" colorizeStrength="100"/>
    <rasterresampler maxOversampling="2"/>
    <resamplingStage>resamplingFilter</resamplingStage>
  </pipe>
  <blendMode>0</blendMode>
</qgis>
