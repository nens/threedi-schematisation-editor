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
    <rasterrenderer nodataColor="" type="singlebandpseudocolor" classificationMin="0" opacity="1" alphaBand="-1" band="1" classificationMax="0.058">
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
        <colorrampshader minimumValue="0" classificationMode="2" maximumValue="0.058" clip="0" labelPrecision="4" colorRampType="INTERPOLATED">
          <colorramp type="gradient" name="[source]">
            <prop k="color1" v="68,1,84,255"/>
            <prop k="color2" v="253,231,37,255"/>
            <prop k="discrete" v="0"/>
            <prop k="rampType" v="gradient"/>
            <prop k="stops" v="0.117647;71,42,122,255:0.215686;63,72,137,255:0.313725;51,99,141,255:0.411765;41,123,142,255:0.509804;32,146,140,255:0.607843;36,170,131,255:0.705882;70,192,111,255:0.803922;124,210,80,255:0.901961;189,223,38,255"/>
          </colorramp>
          <item label="0,0000" color="#440154" alpha="255" value="0"/>
          <item label="0,0064" color="#472778" alpha="255" value="0.00644444425900777"/>
          <item label="0,0129" color="#3e4a89" alpha="255" value="0.0128888885180155"/>
          <item label="0,0193" color="#31688d" alpha="255" value="0.0193333327770233"/>
          <item label="0,0258" color="#26838d" alpha="255" value="0.0257777770360311"/>
          <item label="0,0322" color="#229d88" alpha="255" value="0.0322222212950389"/>
          <item label="0,0387" color="#38b777" alpha="255" value="0.0386666655540466"/>
          <item label="0,0451" color="#6ece58" alpha="255" value="0.0451111098130544"/>
          <item label="0,0516" color="#b5de2b" alpha="255" value="0.0515555540720622"/>
          <item label="0,0580" color="#fde725" alpha="255" value="0.0579999983310699"/>
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
