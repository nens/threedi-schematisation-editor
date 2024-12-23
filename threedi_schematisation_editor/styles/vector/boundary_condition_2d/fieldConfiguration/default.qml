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
    <field configurationFlags="NoFlag" name="timeseries">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="true" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="type">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="1" type="QString" name="1: Water level" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Velocity" />
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Discharge" />
              </Option>
              <Option type="Map">
                <Option value="5" type="QString" name="5: Sommerfeld" />
              </Option>
              <Option type="Map">
                <Option value="6" type="QString" name="6: Groundwater level" />
              </Option>
              <Option type="Map">
                <Option value="7" type="QString" name="7: Groundwater discharge" />
              </Option>
            </Option>
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
    <field configurationFlags="NoFlag" name="tags">
      <editWidget type="TextEdit">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="IsMultiline" />
            <Option value="false" type="bool" name="UseHtml" />
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="time_units">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="seconds" type="QString" name="Seconds" />
              </Option>
              <Option type="Map">
                <Option value="minutes" type="QString" name="Minutes" />
              </Option>
              <Option type="Map">
                <Option value="hours" type="QString" name="Hours" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="interpolate">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>