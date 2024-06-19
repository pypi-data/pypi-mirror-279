from IPython.display import Markdown as render_markdown, HTML as render_html
import os as __os
import json as __json
import re as __re
from uuid import uuid4 as __UUID
import uuid as __uuid

with open(__os.path.join(__os.path.dirname(__file__), "PRELOADED_VARS.md"), "r") as __f:
    PRELOADED_VARS_MARKDOWN = __f.read()


def data_to_markdown(data, col_name_key="Key", col_name_value="Value", title="table"):
    """
    Converts a JSON string or dictionary to a Markdown table.

    Parameters:
        data (str or dict): JSON string or dictionary containing the data.
        col_name_key (str): Custom name for the column header of the keys.
        col_name_value (str): Custom name for the column header of the values.
        title (str): Title of the table.

    Returns:
        str: A Markdown-formatted string representing the table.
    """
    data = __convert_data(data)

    # Start building the Markdown table
    markdown_table = f"{col_name_key} | {col_name_value}\n"  # Table headers
    markdown_table += "---|---\n"  # Separator line for Markdown table

    # Add each key-value pair as a row in the table
    for key, value in data.items():
        # Ensure the value is converted to a string if necessary
        markdown_table += f"{key} | {str(value)}\n"

    return f"## {title}\n{markdown_table}"


COPY_SCRIPT = """ 
<style>
.button {
  background-color: #FFFFFF;
  border: 1px solid rgb(209,213,219);
  border-radius: .5rem;
  box-sizing: border-box;
  color: #111827;
  font-family: "Inter var",ui-sans-serif,system-ui,-apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
  font-size: .875rem;
  font-weight: 300 !important;
  line-height: 1.25rem;
  padding: .25rem 0.5rem !important;
  text-align: center;
  text-decoration: none #D1D5DB solid;
  text-decoration-thickness: auto;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  cursor: pointer;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button:hover {
  background-color: rgb(249,250,251);
}

.button:focus {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

.button:focus-visible {
  box-shadow: none;
}
</style>
<button 
class="button"

onclick='copyTable("REPLACEMENT_HOOK")'>Copy to Clipboard</button>
 <script>

function copyTable(tableId) {
    var table = document.getElementById(tableId);
    if (!table) {
        alert("Table not found!");
        return;
    }
    var rows = table.querySelectorAll('tr');
    var csvContent = '';
    rows.forEach(function(row) {
        var cols = row.querySelectorAll('th, td');
        var rowData = [];
        cols.forEach(function(col) {

                var text = col.innerText.replace(/(\\r\\n|\\n|\\r)/gm, '').trim();
                rowData.push(text);

        });
        // Only add non-empty rows to the CSV content
        if (rowData.length > 0 ) {
            csvContent += rowData.join('\\t') + '\\n';
        }
    });
    // Create a temporary textarea element to copy the content
    var el = document.createElement('textarea');
    el.value = csvContent;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    alert('Copied to clipboard');
}

        </script>"""

STYLES = {
    "table": """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

:root {
    --main-color: #00B6DA; /* Light theme color */
    --table-color: #065F82; /* Light theme table color */
    --accent-color: #FF5500; /* Light theme accent color */
    --foreground-color: #777777; /* Light theme background */
}
.indent-0 { padding-left: 0em; }
.indent-1 { padding-left: 1em; }
.indent-2 { padding-left: 2em; }
.indent-3 { padding-left: 3em; }
.indent-4 { padding-left: 4em; }
.indent-5 { padding-left: 5em; }
.indent-6 { padding-left: 6em; }

@media (prefers-color-scheme: dark) {
    :root {
        --main-color: #0094AC; /* Dark theme color */
        --table-color: #043A4A; /* Dark theme table color */
        --accent-color: #E76F00; /* Dark theme accent color */
        --foreground-color: #777777; /* Dark theme background */
    }
}

body, h1, h2, h3, p {
    font-family: 'Montserrat';
}
table {
    padding: 4px;
    margin-left: 2px;
    margin-right: 2px;
    border-collapse: collapse;
    text-align: center;
    color: #065F82;
    border: 2px solid #ccc; /* Add border */
    border-radius: 10px; /* Add border radius */
    margin-bottom: 20px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Add drop shadow */
    font-weight: semi-bold;
}
h1 {
    font-size: 15px;
    line-height: 30px;
    font-weight: bold;

    color: #00B6DA;
}
h2 {
    font-size: 12px;
    line-height: 16px;
    font-weight: bold;
    
  color: var(--foreground-color);

}
h3 {
    font-size: 12px;
    line-height: 12px;
    font-weight: 600;
    text-align: start
color: var(--foreground-color);

}
p {
    font-size: 12px;
    line-height: 12px;
    font-weight: 500;
color: var(--foreground-color);

}
th, td {
    height: 15px; /* Fixed height for all rows */
    padding: 8px  !important;
    text-align: left !important; /* Ensure text is aligned left */


}
th h2, td h3, td p {
    margin: 0;     /* Remove margin from cell contents */
    padding: 5px;  /* Reduce padding */
    text-align: left; 
    white-space: nowrap; /* Prevent text wrapping */
}

tr:nth-child(even) td {
    border-color: #FF5500;
    color: #FF5500
}
    tr:nth-child(odd) td {
    border-color: #415464;
    color: #FF5500;
}
.muted-text {
    color: #728A9F !important;
}
</style>

"""
}


def __convert_data(data):
    """
    Converts a JSON string to a dictionary if necessary.

    Parameters:
        data (str or dict): JSON string or dictionary containing the data.

    Returns:
        dict: The data as a dictionary.
    """
    # Parse the JSON string into a dictionary if data is a string
    if "to_dict" in dir(data):
        data = data.to_dict()
    if isinstance(data, str):
        try:
            data = __json.loads(data)
        except __json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided.")

    # Ensure data is a dictionary
    if not isinstance(data, dict):
        raise TypeError(
            "Data must be a dictionary or a JSON string representing a dictionary."
        )

    return data


def data_to_html(data, col_name_key="Key", col_name_value="Value", title="table"):
    """
    Returns table HTML representation.

    Parameters:
        data (str or dict): JSON string or dictionary containing the data.
        col_name_key (str): Custom name for the column header of the keys.
        col_name_value (str): Custom name for the column header of the values.
        title (str): Title of the table.
    """

    table = ""

    def format_url(text):
        """ Check if the text is a URL and format it as a hyperlink if true. """
        url_pattern = __re.compile(r'https?://[^\s]+')
        if isinstance(text, str) and url_pattern.match(text):
            return f"<a href='{text}' target='_blank'>{text}</a>"
        return text

    def get_rows(key, value, depth=0,is_list_item=False):
        """ Generate HTML rows for any nested structures, making URLs clickable. """
        rows = ""
        nbsp_indent = "&nbsp;" * (depth * 4)  # Non-breaking spaces for indentation
        indent_class = f"indent-{depth}"  # CSS class for indentation
        muted_class = "muted-text" if depth > 0 or is_list_item else ""

        if isinstance(value, dict):
            # Handle dictionaries by recursively adding rows for each key-value pair
            rows += f"<tr><td class='{indent_class} {muted_class}'>{nbsp_indent}<strong>{key}</strong></td><td></td></tr>"
            for sub_key, sub_value in value.items():
                rows += get_rows(sub_key, sub_value, depth + 1)
        elif isinstance(value, list):
            # Handle lists and check if the first item is a dictionary
            rows += f"<tr><td class='{indent_class} {muted_class}'>{nbsp_indent}<strong>{key}</strong></td><td></td></tr>"
            for item in value:
                if isinstance(item, dict):
                    # Expand dictionary items
                    for sub_key, sub_value in item.items():
                        rows += get_rows(sub_key, sub_value, depth + 1,is_list_item=True)
                else:
                    # Format item as URL if applicable, and handle regular list items
                    formatted_item = format_url(item)
                    rows += f"<tr><td class='{indent_class} muted-text'>{nbsp_indent}</td><td class='muted-text'>{formatted_item}</td></tr>"
        else:
            # Handle simple key-value pairs and format as URL if applicable
            display_value = format_url(value)
            rows += f"<tr><td class='{indent_class} {muted_class}'>{nbsp_indent}<strong>{key}</strong></td><td class='{muted_class}'>{display_value}</td></tr>"

        return rows



    
    def clean(data):
        if isinstance(data, dict):
            return {k: clean(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [clean(item) for item in data if item is not None]
        else:
            return data
    
    # Add each key-value pair as a row in the table
    data = clean(data)
    table = ""
    for key, value in data.items():
        table += get_rows(key, value)

    # Ensure the table ID is correctly set and used in the COPY_SCRIPT
    table_id = f"DATA_TABLE-{__uuid.uuid4()}"  # Unique ID for each table instance
    html_output = f"""<h1>{title}</h1> <table id='{table_id}'><tr><th>{col_name_key}</th><th>{col_name_value}</th></tr>{table}</table>{COPY_SCRIPT.replace('REPLACEMENT_HOOK', table_id)}"""
    return html_output

def render_table(data, col_name_key="Key", col_name_value="Value", title="table"):
    """
    Renders table from data.

    Parameters:
        data (str or dict): JSON string or dictionary containing the data.
        col_name_key (str): Custom name for the column header of the keys.
        col_name_value (str): Custom name for the column header of the values.
        title (str): Title of the table.
    """

    def camel_case_to_spaces(input_string):
        # This regular expression finds all places where a lowercase letter is followed by an uppercase letter
        result = __re.sub(r"(?<=[a-z])(?=[A-Z])", " ", input_string)
        return result

    try:
        if str(type(data)).removeprefix("<class '").split(".")[0] == "lusid":
            title = (
                str(type(data)).split(".")[-1].removesuffix("'>").removeprefix("Create")
            )
            title = camel_case_to_spaces(title)
            col_name_key = "Property"
            col_name_value = "Value"
    except:
        pass
    data = __convert_data(data)
    html_string = data_to_html(data, col_name_key, col_name_value, title)
    styled = (
        "<html><head>"
        + STYLES["table"]
        + "</head><body>"
        + html_string
        + "</body></html>"
    )
    return styled


def display_preloaded_vars():
    """
    Displays the preloaded variables in the current environment.
    """
    return render_markdown(PRELOADED_VARS_MARKDOWN)
