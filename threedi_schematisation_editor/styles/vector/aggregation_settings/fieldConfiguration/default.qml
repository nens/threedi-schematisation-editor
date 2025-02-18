<?xml version='1.0' encoding='utf-8'?>
<qgis><fieldConfiguration>
    <field configurationFlags="NoFlag" name="id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="flow_variable">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="discharge" type="QString" name="discharge: Discharge" />
              </Option>
              <Option type="Map">
                <Option value="flow_velocity" type="QString" name="flow_velocity: Flow velocity" />
              </Option>
              <Option type="Map">
                <Option value="pump_discharge" type="QString" name="pump_discharge: Pump discharge" />
              </Option>
              <Option type="Map">
                <Option value="rain" type="QString" name="rain: Rain" />
              </Option>
              <Option type="Map">
                <Option value="water_level" type="QString" name="water_level: Water level" />
              </Option>
              <Option type="Map">
                <Option value="wet_cross_section" type="QString" name="wet_cross_section: Wet cross sectional area" />
              </Option>
              <Option type="Map">
                <Option value="wet_surface" type="QString" name="wet_surface: Wet surface area" />
              </Option>
              <Option type="Map">
                <Option value="lateral_discharge" type="QString" name="lateral_discharge: Lateral discharge" />
              </Option>
              <Option type="Map">
                <Option value="volume" type="QString" name="volume: Volume" />
              </Option>
              <Option type="Map">
                <Option value="simple_infiltration" type="QString" name="simple_infiltration: Simple infiltration" />
              </Option>
              <Option type="Map">
                <Option value="leakage" type="QString" name="leakage: Leakage" />
              </Option>
              <Option type="Map">
                <Option value="interception" type="QString" name="interception: Interception" />
              </Option>
              <Option type="Map">
                <Option value="surface_source_sink_discharge" type="QString" name="surface_source_sink_discharge: Surface sources and sinks discharge" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="aggregation_method">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="{2839923C-8B7D-419E-B84B-CA2FE9B80EC7}" type="QString" name="" />
              </Option>
              <Option type="Map">
                <Option value="avg" type="QString" name="avg: Average" />
              </Option>
              <Option type="Map">
                <Option value="min" type="QString" name="min: Minimum" />
              </Option>
              <Option type="Map">
                <Option value="max" type="QString" name="max: Maximum" />
              </Option>
              <Option type="Map">
                <Option value="cum" type="QString" name="cum: Cumulative" />
              </Option>
              <Option type="Map">
                <Option value="med" type="QString" name="med: Median" />
              </Option>
              <Option type="Map">
                <Option value="cum_negative" type="QString" name="cum_negative: Cumulative negative" />
              </Option>
              <Option type="Map">
                <Option value="cum_positive" type="QString" name="cum_positive: Cumulative positive" />
              </Option>
              <Option type="Map">
                <Option value="current" type="QString" name="current: Current" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="interval">
      <editWidget type="Range">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="AllowNull" />
            <Option value="2147483647" type="int" name="Max" />
            <Option value="-2147483648" type="int" name="Min" />
            <Option value="0" type="int" name="Precision" />
            <Option value="1" type="int" name="Step" />
            <Option value="SpinBox" type="QString" name="Style" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>