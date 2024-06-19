
[![pypi](https://img.shields.io/pypi/v/lusid-express)](https://pypi.org/project/lusid-express/)
[![python](https://img.shields.io/pypi/pyversions/lusid-express.svg)](https://pypi.org/project/lusid-express/)

# 1. lusid-express
##### 1.0.0.0.1. *`lusid-express` is a python package that makes it quick and easy to get started using Lusid and Luminesce. It is particularly geared toward creating a good notebook user experience when working locally.*



<!-- vscode-markdown-toc -->
* 1. [Getting Started](#GettingStarted)
	* 1.1. [Requirements](#Requirements)
		* 1.1.1. [Environmental Variable setup](#EnvironmentalVariablesetup)
	* 1.2. [Installation](#Installation)
* 2. [Convenience package installations](#Conveniencepackageinstallations)
* 3. [Luminesce Magic Command](#LuminesceMagicCommand)
	* 3.1. [Why use this?](#Whyusethis)
* 4. [Pre-loaded Variables](#Pre-loadedVariables)
* 5. [Formatting](#Formatting)
	* 5.1. [Lusid Objects](#LusidObjects)
	* 5.2. [Copy to Clipboard](#CopytoClipboard)
* 6. [Widgets](#Widgets)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->




This repository holds the source code for lusid-express, a python package that makes it quick and easy to get started using Lusid and Luminesce. The package provides convenience in 4 distinct ways.

1. Ease of installation of finbourne packages.
2.  `%%luminesce` cell magic in your local jupyter installation.
3.  Preset variables that make it possible to ommit boiler plate code.
4.  Widgets and other visual representations of Lusid objects.

```mermaid
flowchart LR

LE-->UTILS[utils]
LE-->WIDGETS[widgets]
LE-->MAIN[CLI]
LE[lusid_express]-->API[apis]
LE-->DISPLAY[display]




WIDGETS-->Transaction(Transaction Forms):::F
MAIN-->O(Optional Styling Overrides):::F
MAIN-->Vars(Optional startup variables):::F
MAIN-->Mag(Optional magics):::F
DISPLAY-->M(markdown render tools):::F
DISPLAY-->H(HTML render tools):::F
DISPLAY-->S(Styling):::F
DISPLAY-->Scr(javaScript):::F
API-->Ap(authed lusid apis):::F
UTILS-->L(datetime tools):::F
UTILS-->V(case adjustment tools):::F
UTILS-->X(idempotentcy tools):::F

classDef F fill:#e1dddd
```

##  1. <a name='GettingStarted'></a>Getting Started
###  1.1. <a name='Requirements'></a>Requirements
In order to authenticate the lusid api clients you will need to have generated a secrets file. furthermore, you will need to have an environmental variable named `FBN_SECRETS_PATH` set to the full path to your secrets file. 

####  1.1.1. <a name='EnvironmentalVariablesetup'></a>Environmental Variable setup
##### 1.1.1.1.1. Mac OS
Assuming `~/.secret/secrets.json` exists
```bash
echo 'export FBN_SECRETS_PATH="~/.secret/secrets.json"' >> ~/.zshrc
```


NOTE: Your secrets file needs to include the lumi api url under the key: `lumiApiUrl`. This url usually takes the form `https://{your-domain}.lusid.com/honeycomb`.

###  1.2. <a name='Installation'></a>Installation 

```sh
pip install -U lusid-express
python -m lusid_express --enable all
```
 The above commands install the `lusid-express` package and enable enhancements to your IPython environment. If running from a virtual environment these enhancements are limited to that virtual environment.
 enabling `magic` adds the `luminesce` magic command. `vars` adds preloaded variables to IPython sessions. `format` adds tables with finbourne branding, as well as branded automatic rendering of lusid objects when displayed. The `--disable` command is available should you wish to disable these. 




##  2. <a name='Conveniencepackageinstallations'></a>Convenience package installations

```mermaid
graph LR;
    lu[lusid_express]-->lusid_express[Lusid_blundle]
    lusid_express --> luminesce_sdk_preview
    lusid_express --> lusid_jam
    lusid_express --> lusid_sdk_preview
    lusid_express --> fbnlab_preview
    lusid_express --> finbourne_access_sdk
    lusid_express --> finbourne_identity_sdk
    lusid_express --> finbourne_insights_sdk_preview
    lusid_express --> finbourne_sdk_utilities
    lusid_express --> lusid_configuration_sdk_preview
    lusid_express --> lusid_drive_sdk_preview
    lusid_express --> lusid_notifications_sdk_preview
    lusid_express --> lusid_scheduler_sdk_preview
    lusid_express --> lusid_workflow_sdk_preview
    lusid_express --> lusidtools
    lusid_express --> dve_lumipy_preview

    luminesce_sdk_preview["luminesce-sdk-preview==1.14.758"]
    lusid_jam["lusid-jam==0.1.2"]
    lusid_sdk_preview["lusid-sdk-preview==1.1.120"]
    fbnlab_preview["fbnlab-preview==0.1.108"]
    finbourne_access_sdk["finbourne-access-sdk==0.0.3751"]
    finbourne_identity_sdk["finbourne-identity-sdk==0.0.2834"]
    finbourne_insights_sdk_preview["finbourne-insights-sdk-preview==0.0.763"]
    finbourne_sdk_utilities["finbourne-sdk-utilities==0.0.10"]
    lusid_configuration_sdk_preview["lusid-configuration-sdk-preview==0.1.514"]
    lusid_drive_sdk_preview["lusid-drive-sdk-preview==0.1.617"]
    lusid_notifications_sdk_preview["lusid-notifications-sdk-preview==0.1.923"]
    lusid_scheduler_sdk_preview["lusid-scheduler-sdk-preview==0.0.829"]
    lusid_workflow_sdk_preview["lusid-workflow-sdk-preview==0.1.810"]
    lusidtools["lusidtools==1.0.14"]
    dve_lumipy_preview["dve-lumipy-preview==0.1.1075"]

```


##  3. <a name='LuminesceMagicCommand'></a>Luminesce Magic Command

```bash
python -m lusid_express -e magic
```

###  3.1. <a name='Whyusethis'></a>Why use this?
The main motivation to use this cell magic is to enable SQL syntax highlighting through the use of SQL jupyter cells. That is, rather than display a cell on a notebook that holds an SQL string such as:
```python
sql_string = """
@raw_equities =
SELECT *,
    'training' as Scope,
    Currency as domCcy,
    Ticker as DisplayName
FROM @equitiesCSV
WHERE Ticker IS NOT null;
where Ticker is null
    and "type" is not "FundsIn";
SELECT *
FROM Lusid.Instrument.Equity.Writer
WHERE toWrite = @raw_equities;
"""

```

You would instead have a cell with pure SQL that looks like this:
```SQL
%%luminesce

@raw_equities =
SELECT *,
    'training' as Scope,
    Currency as domCcy,
    Ticker as DisplayName
FROM @equitiesCSV
WHERE Ticker IS NOT null;
where Ticker is null
    and "type" is not "FundsIn";
SELECT *
FROM Lusid.Instrument.Equity.Writer
WHERE toWrite = @raw_equities;
```
VSCode allows the SQL auto-formatting of Jupyter cells. This query runs when the cell is excecuted.



##  4. <a name='Pre-loadedVariables'></a>Pre-loaded Variables
```bash
python -m lusid_express -e vars
```
Enabling this feature provides the convenience of automatically loading important variables into python notebooks. This allows us to omit boler-plate code from each notebook. It also allows for reduce complexity as token management, authentication, and api client instantiations have all been abstracted away.

| Variable Name | Statement         | Description                          |
|---------------|-------------------|--------------------------------------|
| lu          | `import lusid as lu` | Main LUSID package                   |
| lm          | `import lusid.models as lm` | LUSID models module                  |
| apis         | `import lusid_express.apis as apis` | convenience package providing pre-authenticated api access.                 |


##  5. <a name='Formatting'></a>Formatting

```bash
python -m lusid_express -e format
```
When enabled, `format` overrides default rendering of certain types of objects.

###  5.1. <a name='LusidObjects'></a>Lusid Objects
Lusid Objects are rendered as tables, displaying the object type as the table's title, and its properties in the table's rows

<h4>Equity</h4> <table id='DATA_TABLE-f8224859-f897-42c9-ae2a-df56f52dda23'><tr><th>Property</th><th>Value</th></tr><tr><td class='indent-0 '><strong>identifiers</strong></td><td></td></tr><tr><td class='indent-1 muted-text'>&nbsp;&nbsp;&nbsp;&nbsp;<strong>isin</strong></td><td class='muted-text'>US0378331005</td></tr><tr><td class='indent-1 muted-text'>&nbsp;&nbsp;&nbsp;&nbsp;<strong>figi</strong></td><td class='muted-text'>BBG000B9XVV8</td></tr><tr><td class='indent-1 muted-text'>&nbsp;&nbsp;&nbsp;&nbsp;<strong>ticker</strong></td><td class='muted-text'>AAPL</td></tr><tr><td class='indent-0 '><strong>dom_ccy</strong></td><td class=''>USD</td></tr><tr><td class='indent-0 '><strong>instrument_type</strong></td><td class=''>Equity</td></tr></table> 

###  5.2. <a name='CopytoClipboard'></a>Copy to Clipboard
With every table or Pandas DataFrame a `Copy to Clipboard` button is available for excel friendly copy/pasting.

##  6. <a name='Widgets'></a>Widgets
The widgets module allows you to quickly create forms that represent the input of several entity types. They also include a submit button to execute api calls. Only `Transactions` have a widget representation for now, more will be added.
