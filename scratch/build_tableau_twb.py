"""
Generator script for Tableau Workbook (.twb) XML file.
Creates a valid, professional Tableau Workbook pointing to tableau_energy_dataset.csv.
"""

from pathlib import Path


def generate_twb_file():
    project_root = Path(__file__).resolve().parent.parent
    tableau_dir = project_root / "tableau"
    twb_path = tableau_dir / "Energy_Consumption_Dashboard.twb"

    twb_xml = """<?xml version='1.0' encoding='utf-8' ?>
<workbook version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='24' />
  </preferences>
  <datasources>
    <datasource caption='Tableau Energy Dataset' inline='true' name='federated.tableau_energy_dataset' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='tableau_energy_dataset' name='textscan.tableau_energy_dataset'>
            <connection class='textscan' directory='.' filename='tableau_energy_dataset.csv' password='' server='' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.tableau_energy_dataset' name='tableau_energy_dataset.csv' table='[tableau_energy_dataset#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=','>
            <column datatype='datetime' name='date' ordinal='0' />
            <column datatype='integer' name='Appliances' ordinal='1' />
            <column datatype='integer' name='lights' ordinal='2' />
            <column datatype='real' name='T1' ordinal='3' />
            <column datatype='real' name='RH_1' ordinal='4' />
            <column datatype='real' name='T2' ordinal='5' />
            <column datatype='real' name='RH_2' ordinal='6' />
            <column datatype='real' name='T3' ordinal='7' />
            <column datatype='real' name='RH_3' ordinal='8' />
            <column datatype='real' name='T4' ordinal='9' />
            <column datatype='real' name='RH_4' ordinal='10' />
            <column datatype='real' name='T5' ordinal='11' />
            <column datatype='real' name='RH_5' ordinal='12' />
            <column datatype='real' name='T6' ordinal='13' />
            <column datatype='real' name='RH_6' ordinal='14' />
            <column datatype='real' name='T7' ordinal='15' />
            <column datatype='real' name='RH_7' ordinal='16' />
            <column datatype='real' name='T8' ordinal='17' />
            <column datatype='real' name='RH_8' ordinal='18' />
            <column datatype='real' name='T9' ordinal='19' />
            <column datatype='real' name='RH_9' ordinal='20' />
            <column datatype='real' name='T_out' ordinal='21' />
            <column datatype='real' name='Press_mm_hg' ordinal='22' />
            <column datatype='real' name='RH_out' ordinal='23' />
            <column datatype='real' name='Windspeed' ordinal='24' />
            <column datatype='real' name='Visibility' ordinal='25' />
            <column datatype='real' name='Tdewpoint' ordinal='26' />
            <column datatype='real' name='rv1' ordinal='27' />
            <column datatype='real' name='rv2' ordinal='28' />
            <column datatype='integer' name='year' ordinal='29' />
            <column datatype='integer' name='month' ordinal='30' />
            <column datatype='string' name='month_name' ordinal='31' />
            <column datatype='integer' name='day' ordinal='32' />
            <column datatype='integer' name='day_of_week' ordinal='33' />
            <column datatype='string' name='day_name' ordinal='34' />
            <column datatype='integer' name='hour' ordinal='35' />
            <column datatype='integer' name='is_weekend' ordinal='36' />
            <column datatype='real' name='predicted_Appliances' ordinal='37' />
            <column datatype='string' name='record_type' ordinal='38' />
          </columns>
        </relation>
      </connection>
    </datasource>
  </datasources>
  <worksheets>
    <worksheet name='KPI Overview'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.tableau_energy_dataset' />
          </datasources>
          <aggregation value='true' />
        </view>
        <style />
        <panes>
          <pane>
            <x-axis name='[federated.tableau_energy_dataset].[sum:Appliances:qk]' />
          </pane>
        </panes>
      </table>
    </worksheet>
    <worksheet name='Energy Demand Trend &amp; Forecast'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.tableau_energy_dataset' />
          </datasources>
          <aggregation value='true' />
        </view>
        <style />
      </table>
    </worksheet>
    <worksheet name='Hourly &amp; Weekend Patterns'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.tableau_energy_dataset' />
          </datasources>
          <aggregation value='true' />
        </view>
        <style />
      </table>
    </worksheet>
    <worksheet name='Actual vs Predicted (Model Evaluation)'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.tableau_energy_dataset' />
          </datasources>
          <aggregation value='true' />
        </view>
        <style />
      </table>
    </worksheet>
  </worksheets>
  <dashboards>
    <dashboard name='Energy Consumption Forecasting &amp; Analytics Dashboard'>
      <style />
      <size maxheight='1080' maxwidth='1920' minheight='800' minwidth='1200' />
      <zones>
        <zone h='100000' id='1' type='layout-basic' w='100000' x='0' y='0'>
          <zone h='10000' id='2' name='KPI Overview' type='sheet' w='100000' x='0' y='0' />
          <zone h='45000' id='3' name='Energy Demand Trend &amp; Forecast' type='sheet' w='100000' x='0' y='10000' />
          <zone h='45000' id='4' name='Hourly &amp; Weekend Patterns' type='sheet' w='50000' x='0' y='55000' />
          <zone h='45000' id='5' name='Actual vs Predicted (Model Evaluation)' type='sheet' w='50000' x='50000' y='55000' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>
  <windows>
    <window class='dashboard' name='Energy Consumption Forecasting &amp; Analytics Dashboard'>
      <active pane='1' />
    </window>
  </windows>
</workbook>
"""
    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(twb_xml)
    print(f"Created Tableau Workbook file: {twb_path}")


if __name__ == "__main__":
    generate_twb_file()
