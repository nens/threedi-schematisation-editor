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
    <field configurationFlags="NoFlag" name="action_table">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="action_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="set_crest_level" type="QString" name="Set crest level" />
              </Option>
              <Option type="Map">
                <Option value="set_discharge_coefficients" type="QString" name="Set discharge coefficients" />
              </Option>
              <Option type="Map">
                <Option value="set_gate_level" type="QString" name="Set gate level" />
              </Option>
              <Option type="Map">
                <Option value="set_pump_capacity" type="QString" name="Set pump capacity" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="measure_operator">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="&gt;" type="QString" name="&gt;" />
              </Option>
              <Option type="Map">
                <Option value="&lt;" type="QString" name="&lt;" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="target_type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="pump" type="QString" name="Pump" />
              </Option>
              <Option type="Map">
                <Option value="orifice" type="QString" name="Orifice" />
              </Option>
              <Option type="Map">
                <Option value="weir" type="QString" name="Weir" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="target_id">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="tags">
      <editWidget type="JsonEdit">
        <config>
          <Option type="Map">
            <Option value="0" type="int" name="DefaultView" />
            <Option value="0" type="int" name="FormatJson" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="code">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="display_name">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>