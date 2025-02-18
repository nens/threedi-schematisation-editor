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
    <field configurationFlags="NoFlag" name="use_advection_1d">
      <editWidget type="ValueMap">
        <config>
          <Option type="Map">
            <Option type="List" name="map">
              <Option type="Map">
                <Option value="0" type="QString" name="0: No 1D advection" />
              </Option>
              <Option type="Map">
                <Option value="1" type="QString" name="1: Momentum conservative scheme" />
              </Option>
              <Option type="Map">
                <Option value="2" type="QString" name="2: Energy conservative scheme" />
              </Option>
              <Option type="Map">
                <Option value="3" type="QString" name="3: Combined momentum and energy conservative scheme" />
              </Option>
            </Option>
          </Option>
        </config>
      </editWidget>
    </field>
    <field configurationFlags="NoFlag" name="use_advection_2d">
      <editWidget type="CheckBox">
        <config>
          <Option type="Map">
            <Option value="false" type="bool" name="AllowNullState" />
            <Option value="1" type="QString" name="CheckedState" />
            <Option value="0" type="int" name="TextDisplayMethod" />
            <Option value="0" type="QString" name="UncheckedState" />
          </Option>
        </config>
      </editWidget>
    </field>
  </fieldConfiguration>
  </qgis>