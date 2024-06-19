import ipywidgets as widgets
from IPython.display import display, HTML
from datetime import datetime
from ..apis import transaction_portfolios_api
import lusid as lu  # Import your lusid library
import lusid.models as lm  # Import the models from the lusid library

# Custom CSS styling
custom_css = """
<style>
    .form-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        max-width: 600px; /* Set a reasonable maximum width for the form */
        margin: 0 auto; /* Center the form horizontally */
        background-color: #f9f9f9; /* Background color */
        border: 1px solid #ccc; /* Border color */
        border-radius: 10px; /* Rounded border */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Drop shadow */
        padding: 20px; /* Padding inside the form */
    }
    .form-row {
        display: flex;
        align-items: center;
    }
    .form-label {
        width: 200px; /* Fixed width for labels */
        font-weight: bold;
        color: #4a4a4a;
        text-align: left;
    }
    .form-field {
        width: 100%; /* Full width within the container */
        max-width: 350px; /* Set maximum width for fields */
        background-color: #f0f0f0;
        border-radius: 4px;
        padding: 8px;
        border: 1px solid #ccc; /* Border color for fields */
    }
    .widget-button-success {
        background-color: #28a745;
        color: white;
    }
    .widget-button-success:hover {
        background-color: #218838;
    }
</style>
"""


class TransactionForm:
    def __init__(self, txn, scope, portfolio_code):
        self.txn = txn
        self.scope = scope
        self.portfolio_code = portfolio_code
        self.create_transaction_form(txn)

    def create_transaction_form(self, txn: lu.TransactionRequest):
        # Default values derived from the variables
        default_transaction_id = txn.transaction_id
        default_type = txn.type
        default_source = txn.source
        default_instrument_identifier_types = list(txn.instrument_identifiers.keys())[0]
        default_instrument_identifiers = list(txn.instrument_identifiers.values())[0]
        default_transaction_date = txn.transaction_date
        default_settlement_date = txn.settlement_date
        default_units = txn.units
        default_transaction_currency = txn.transaction_currency
        default_amount = txn.total_consideration.amount
        default_settlement_currency = txn.total_consideration.currency
        default_properties = txn.properties

        # Create widgets with custom layout for labels and fields
        label_layout = widgets.Layout(
            width="200px",
        )  # Adjust width as needed
        field_layout = widgets.Layout(width="350px")  # Adjust to fit the form container

        transaction_id = widgets.Text(
            value=default_transaction_id,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        type = widgets.Text(
            value=default_type,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        source = widgets.Text(
            value=default_source,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        instrument_identifiers = widgets.Text(
            value=default_instrument_identifiers,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        transaction_date = widgets.DatePicker(
            value=datetime.strptime(default_transaction_date, "%Y-%m-%d"),
            layout=field_layout,
            style={"description_width": "initial"},
        )
        settlement_date = widgets.DatePicker(
            value=datetime.strptime(default_settlement_date, "%Y-%m-%d"),
            layout=field_layout,
            style={"description_width": "initial"},
        )
        units = widgets.IntText(
            value=default_units,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        transaction_currency = widgets.Text(
            value=default_transaction_currency,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        amount = widgets.FloatText(
            value=default_amount,
            layout=field_layout,
            style={"description_width": "initial"},
        )
        settlement_currency = widgets.Text(
            value=default_settlement_currency,
            layout=field_layout,
            style={"description_width": "initial"},
        )

        def get_prop_widget(prop):
            if (
                "label_value" in prop.value.attribute_map
                and prop.value.label_value is not None
            ):
                value = prop.value.label_value
                return widgets.Text(
                    value=value,
                    layout=field_layout,
                    style={"description_width": "initial"},
                )
            elif (
                "metric_value" in prop.value.attribute_map
                and prop.value.metric_value.value is not None
            ):
                value = prop.value.metric_value.value
                return widgets.FloatText(
                    value=value,
                    layout=field_layout,
                    style={"description_width": "initial"},
                )
            else:
                return None

        propwidgs = [get_prop_widget(prop) for prop in default_properties.values()]
        submit_button = widgets.Button(description="Submit", button_style="success")

        # Function to create the transaction request based on user input
        def create_transaction_request():
            props = {}
            for k, p in zip(default_properties.keys(), propwidgs):
                # if input string is a number, convert to float
                try:
                    props[k] = lm.PerpetualProperty(
                        key=k,
                        value=lm.PropertyValue(
                            metric_value=lm.MetricValue(value=float(p.value))
                        ),
                    )
                except ValueError:
                    props[k] = lm.PerpetualProperty(
                        key=k, value=lm.PropertyValue(label_value=p.value)
                    )

            txn_ = lm.TransactionRequest(
                transaction_id=transaction_id.value,
                type=type.value,
                source=source.value,
                instrument_identifiers={
                    default_instrument_identifier_types: instrument_identifiers.value
                },
                transaction_date=transaction_date.value.strftime("%Y-%m-%d"),
                settlement_date=settlement_date.value.strftime("%Y-%m-%d"),
                units=units.value,
                transaction_currency=transaction_currency.value,
                total_consideration=lm.CurrencyAndAmount(
                    amount=amount.value, currency=settlement_currency.value
                ),
                properties=props,
            )
            return txn_

        # Function to handle button click
        def on_button_click(b):
            transaction_request = create_transaction_request()
            display(
                transaction_portfolios_api.upsert_transactions(
                    scope=self.scope,
                    code=self.portfolio_code,
                    transaction_request=[transaction_request],
                )
            )

        submit_button.on_click(on_button_click)

        prop_widg_box = [
            widgets.HBox(
                [widgets.Label(k.split("/")[-1], layout=label_layout), prop],
                layout=widgets.Layout(width="100%"),
            )
            for k, prop in zip(default_properties.keys(), propwidgs)
        ]
        # Display widgets with custom CSS
        display(HTML(custom_css))
        form_container = widgets.VBox(
            [
                widgets.HBox(
                    [
                        widgets.Label("Transaction ID:", layout=label_layout),
                        transaction_id,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [widgets.Label("Type:", layout=label_layout), type],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [widgets.Label("Source:", layout=label_layout), source],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [
                        widgets.Label(
                            f"{default_instrument_identifier_types}:",
                            layout=label_layout,
                        ),
                        instrument_identifiers,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [
                        widgets.Label("Transaction Date:", layout=label_layout),
                        transaction_date,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [
                        widgets.Label("Settlement Date:", layout=label_layout),
                        settlement_date,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [widgets.Label("Units:", layout=label_layout), units],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [
                        widgets.Label("Transaction Currency:", layout=label_layout),
                        transaction_currency,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [widgets.Label("Amount:", layout=label_layout), amount],
                    layout=widgets.Layout(width="100%"),
                ),
                widgets.HBox(
                    [
                        widgets.Label("Settlement Currency:", layout=label_layout),
                        settlement_currency,
                    ],
                    layout=widgets.Layout(width="100%"),
                ),
                *prop_widg_box,
                submit_button,
            ],
            layout=widgets.Layout(
                align_items="flex-start",
                padding="20px",
                border="1px solid #ccc",
                border_radius="10px",
                box_shadow="0 4px 8px rgba(0, 0, 0, 0.1)",
                background_color="#f9f9f9",
            ),
        )
        display(form_container)
