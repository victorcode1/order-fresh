import json
input_data = {"data": {
  "id": 42416,
  "parent_id": 0,
  "status": "processing",
  "currency": "USD",
  "version": "7.2.2",
  "prices_include_tax": False,
  "date_created": "2023-01-06T15:42:40",
  "date_modified": "2023-01-06T15:42:40",
  "discount_total": "0.00",
  "discount_tax": "0.00",
  "shipping_total": "0.00",
  "shipping_tax": "0.00",
  "cart_tax": "0.00",
  "total": "0.00",
  "total_tax": "0.00",
  "customer_id": 0,
  "order_key": "wc_order_rNe3EtOTU4tPL",
  "billing": {
    "first_name": "Avery",
    "last_name": "Stampp",
    "company": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "state": "",
    "postcode": "",
    "country": "",
    "email": "",
    "phone": "2034917378"
  },
  "shipping": {
    "first_name": "",
    "last_name": "",
    "company": "",
    "address_1": "",
    "address_2": "",
    "city": "",
    "state": "",
    "postcode": "",
    "country": "",
    "phone": ""
  },
  "payment_method": "",
  "payment_method_title": "",
  "transaction_id": "",
  "customer_ip_address": "71.26.170.235",
  "customer_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
  "created_via": "checkout",
  "customer_note": "",
  "date_completed": None,
  "date_paid": "2023-01-06T15:42:40",
  "cart_hash": "efc22f2eaff8ce503960fe5a4c19e7f0",
  "number": "42416",
  "meta_data": [
    {
      "id": 445144,
      "key": "is_vat_exempt",
      "value": "no"
    },
    {
      "id": 445145,
      "key": "delivery_type",
      "value": "pickup"
    },
    {
      "id": 445146,
      "key": "pickup_date",
      "value": "2023-01-06"
    },
    {
      "id": 445147,
      "key": "pickup_time",
      "value": "15:50 - 16:00"
    }
  ],
  "line_items": [
    {
      "id": 193,
      "name": "Boar's Head Corned Beef Brisket",
      "product_id": 42313,
      "variation_id": 0,
      "quantity": 1,
      "tax_class": "",
      "subtotal": "0.00",
      "subtotal_tax": "0.00",
      "total": "0.00",
      "total_tax": "0.00",
      "taxes": [],
      "meta_data": [
        {
          "id": 2437,
          "key": "CHOOSE WEIGHT OR BY THE SLICE",
          "value": "Slice",
          "display_key": "CHOOSE WEIGHT OR BY THE SLICE",
          "display_value": "Slice"
        },
        {
          "id": 2438,
          "key": "Slices (1-10)",
          "value": "1",
          "display_key": "Slices (1-10)",
          "display_value": "1"
        },
        {
          "id": 2439,
          "key": "SELECT YOUR THICKNESS",
          "value": "Normal",
          "display_key": "SELECT YOUR THICKNESS",
          "display_value": "Normal"
        },
        {
          "id": 2440,
          "key": "_wapf_meta",
          "value": {
            "fields": {
              "63a209501697f": {
                "id": "63a209501697f",
                "type": "radio",
                "label": "CHOOSE WEIGHT OR BY THE SLICE",
                "value": "Slice",
                "values": [
                  {
                    "label": "Slice",
                    "price": 0,
                    "price_type": "none",
                    "slug": "tsthm"
                  }
                ]
              },
              "63a20831280ce": {
                "id": "63a20831280ce",
                "type": "number",
                "label": "Slices (1-10)",
                "value": "1",
                "values": [
                  {
                    "label": "1",
                    "price": 0,
                    "price_type": "none"
                  }
                ]
              },
              "63a210de38782": {
                "id": "63a210de38782",
                "type": "image-swatch",
                "label": "SELECT YOUR THICKNESS",
                "value": "Normal",
                "values": [
                  {
                    "label": "Normal",
                    "price": 0,
                    "price_type": "none",
                    "slug": "jpstg"
                  }
                ]
              }
            },
            "settings": {
              "CHOOSE WEIGHT OR BY THE SLICE": [
                {
                  "field": "63a209501697f",
                  "hide": True
                }
              ],
              "Slices (1-10)": [
                {
                  "field": "63a20831280ce",
                  "hide": False
                }
              ],
              "SELECT YOUR THICKNESS": [
                {
                  "field": "63a210de38782",
                  "hide": False
                }
              ]
            }
          },
          "display_key": "_wapf_meta",
          "display_value": {
            "fields": {
              "63a209501697f": {
                "id": "63a209501697f",
                "type": "radio",
                "label": "CHOOSE WEIGHT OR BY THE SLICE",
                "value": "Slice",
                "values": [
                  {
                    "label": "Slice",
                    "price": 0,
                    "price_type": "none",
                    "slug": "tsthm"
                  }
                ]
              },
              "63a20831280ce": {
                "id": "63a20831280ce",
                "type": "number",
                "label": "Slices (1-10)",
                "value": "1",
                "values": [
                  {
                    "label": "1",
                    "price": 0,
                    "price_type": "none"
                  }
                ]
              },
              "63a210de38782": {
                "id": "63a210de38782",
                "type": "image-swatch",
                "label": "SELECT YOUR THICKNESS",
                "value": "Normal",
                "values": [
                  {
                    "label": "Normal",
                    "price": 0,
                    "price_type": "none",
                    "slug": "jpstg"
                  }
                ]
              }
            },
            "settings": {
              "CHOOSE WEIGHT OR BY THE SLICE": [
                {
                  "field": "63a209501697f",
                  "hide": True
                }
              ],
              "Slices (1-10)": [
                {
                  "field": "63a20831280ce",
                  "hide": False
                }
              ],
              "SELECT YOUR THICKNESS": [
                {
                  "field": "63a210de38782",
                  "hide": False
                }
              ]
            }
          }
        }
      ],
      "sku": "70081",
      "price": 0,
      "image": {
        "id": "42329",
        "src": "https://caraluzzis.com/wp-content/uploads/2023/01/BH-Corned-Beef.jpg"
      },
      "parent_name": None
    },
    {
      "id": 194,
      "name": "Buffalo Chicken Ranch",
      "product_id": 42401,
      "variation_id": 0,
      "quantity": 1,
      "tax_class": "",
      "subtotal": "0.00",
      "subtotal_tax": "0.00",
      "total": "0.00",
      "total_tax": "0.00",
      "taxes": [],
      "meta_data": [
        {
          "id": 2450,
          "key": "Select your size.",
          "value": "Half $6.99",
          "display_key": "Select your size.",
          "display_value": "Half $6.99"
        },
        {
          "id": 2451,
          "key": "Modify your sub?",
          "value": "True",
          "display_key": "Modify your sub?",
          "display_value": "True"
        },
        {
          "id": 2452,
          "key": "Cheese (select up to 2)",
          "value": "American Cheese, Cheddar Cheese",
          "display_key": "Cheese (select up to 2)",
          "display_value": "American Cheese, Cheddar Cheese"
        },
        {
          "id": 2453,
          "key": "Condiments (select up to 2)",
          "value": "Ranch Dressing, Horseradish Sauce",
          "display_key": "Condiments (select up to 2)",
          "display_value": "Ranch Dressing, Horseradish Sauce"
        },
        {
          "id": 2454,
          "key": "Toppings",
          "value": "Shredded Lettuce, Tomato, Sliced Jalapeno",
          "display_key": "Toppings",
          "display_value": "Shredded Lettuce, Tomato, Sliced Jalapeno"
        },
        {
          "id": 2455,
          "key": "_wapf_meta",
          "value": {
            "fields": {
              "63b868afde26e": {
                "id": "63b868afde26e",
                "type": "radio",
                "label": "Select your size.",
                "value": "Half $6.99",
                "values": [
                  {
                    "label": "Half $6.99",
                    "price": 0,
                    "price_type": "none",
                    "slug": "ow7v8"
                  }
                ]
              },
              "63b868afde3a4": {
                "id": "63b868afde3a4",
                "type": "True-False",
                "label": "Modify your sub?",
                "value": "True",
                "values": [
                  {
                    "label": "True",
                    "price": 0,
                    "price_type": "none"
                  }
                ]
              },
              "63b868afde3ba": {
                "id": "63b868afde3ba",
                "type": "checkboxes",
                "label": "Cheese (select up to 2)",
                "value": "American Cheese, Cheddar Cheese",
                "values": [
                  {
                    "label": "American Cheese",
                    "price": 0,
                    "price_type": "none",
                    "slug": "jy8gn"
                  },
                  {
                    "label": "Cheddar Cheese",
                    "price": 0,
                    "price_type": "none",
                    "slug": "6look"
                  }
                ]
              },
              "63b868afde3cd": {
                "id": "63b868afde3cd",
                "type": "checkboxes",
                "label": "Condiments (select up to 2)",
                "value": "Ranch Dressing, Horseradish Sauce",
                "values": [
                  {
                    "label": "Ranch Dressing",
                    "price": 0,
                    "price_type": "none",
                    "slug": "2e5ou"
                  },
                  {
                    "label": "Horseradish Sauce",
                    "price": 0,
                    "price_type": "none",
                    "slug": "r0nr7"
                  }
                ]
              },
              "63b868afde3e1": {
                "id": "63b868afde3e1",
                "type": "checkboxes",
                "label": "Toppings",
                "value": "Shredded Lettuce, Tomato, Sliced Jalapeno",
                "values": [
                  {
                    "label": "Shredded Lettuce",
                    "price": 0,
                    "price_type": "none",
                    "slug": "2pf2r"
                  },
                  {
                    "label": "Tomato",
                    "price": 0,
                    "price_type": "none",
                    "slug": "pd6pj"
                  },
                  {
                    "label": "Sliced Jalapeno",
                    "price": 0,
                    "price_type": "none",
                    "slug": "awsyy"
                  }
                ]
              }
            },
            "settings": {
              "Select your size.": [
                {
                  "field": "63b868afde26e",
                  "hide": False
                }
              ],
              "Modify your sub?": [
                {
                  "field": "63b868afde3a4",
                  "hide": True
                }
              ],
              "Cheese (select up to 2)": [
                {
                  "field": "63b868afde3ba",
                  "hide": False
                }
              ],
              "Condiments (select up to 2)": [
                {
                  "field": "63b868afde3cd",
                  "hide": False
                }
              ],
              "Toppings": [
                {
                  "field": "63b868afde3e1",
                  "hide": False
                }
              ]
            }
          },
          "display_key": "_wapf_meta",
          "display_value": {
            "fields": {
              "63b868afde26e": {
                "id": "63b868afde26e",
                "type": "radio",
                "label": "Select your size.",
                "value": "Half $6.99",
                "values": [
                  {
                    "label": "Half $6.99",
                    "price": 0,
                    "price_type": "none",
                    "slug": "ow7v8"
                  }
                ]
              },
              "63b868afde3a4": {
                "id": "63b868afde3a4",
                "type": "True-False",
                "label": "Modify your sub?",
                "value": "True",
                "values": [
                  {
                    "label": "True",
                    "price": 0,
                    "price_type": "none"
                  }
                ]
              },
              "63b868afde3ba": {
                "id": "63b868afde3ba",
                "type": "checkboxes",
                "label": "Cheese (select up to 2)",
                "value": "American Cheese, Cheddar Cheese",
                "values": [
                  {
                    "label": "American Cheese",
                    "price": 0,
                    "price_type": "none",
                    "slug": "jy8gn"
                  },
                  {
                    "label": "Cheddar Cheese",
                    "price": 0,
                    "price_type": "none",
                    "slug": "6look"
                  }
                ]
              },
              "63b868afde3cd": {
                "id": "63b868afde3cd",
                "type": "checkboxes",
                "label": "Condiments (select up to 2)",
                "value": "Ranch Dressing, Horseradish Sauce",
                "values": [
                  {
                    "label": "Ranch Dressing",
                    "price": 0,
                    "price_type": "none",
                    "slug": "2e5ou"
                  },
                  {
                    "label": "Horseradish Sauce",
                    "price": 0,
                    "price_type": "none",
                    "slug": "r0nr7"
                  }
                ]
              },
              "63b868afde3e1": {
                "id": "63b868afde3e1",
                "type": "checkboxes",
                "label": "Toppings",
                "value": "Shredded Lettuce, Tomato, Sliced Jalapeno",
                "values": [
                  {
                    "label": "Shredded Lettuce",
                    "price": 0,
                    "price_type": "none",
                    "slug": "2pf2r"
                  },
                  {
                    "label": "Tomato",
                    "price": 0,
                    "price_type": "none",
                    "slug": "pd6pj"
                  },
                  {
                    "label": "Sliced Jalapeno",
                    "price": 0,
                    "price_type": "none",
                    "slug": "awsyy"
                  }
                ]
              }
            },
            "settings": {
              "Select your size.": [
                {
                  "field": "63b868afde26e",
                  "hide": False
                }
              ],
              "Modify your sub?": [
                {
                  "field": "63b868afde3a4",
                  "hide": True
                }
              ],
              "Cheese (select up to 2)": [
                {
                  "field": "63b868afde3ba",
                  "hide": False
                }
              ],
              "Condiments (select up to 2)": [
                {
                  "field": "63b868afde3cd",
                  "hide": False
                }
              ],
              "Toppings": [
                {
                  "field": "63b868afde3e1",
                  "hide": False
                }
              ]
            }
          }
        }
      ],
      "sku": "SS 011",
      "price": 0,
      "image": {
        "id": "",
        "src": ""
      },
      "parent_name": None
    }
  ],
  "tax_lines": [],
  "shipping_lines": [],
  "fee_lines": [],
  "coupon_lines": [],
  "refunds": [],
  "payment_url": "https://caraluzzis.com/checkout/order-pay/42416/?pay_for_order=True&key=wc_order_rNe3EtOTU4tPL",
  "is_editable": False,
  "needs_payment": False,
  "needs_processing": True,
  "date_created_gmt": "2023-01-06T20:42:40",
  "date_modified_gmt": "2023-01-06T20:42:40",
  "date_completed_gmt": None,
  "date_paid_gmt": "2023-01-06T20:42:40",
  "currency_symbol": "$",
  "_links": {
    "self": [
      {
        "href": "https://caraluzzis.com/wp-json/wc/v3/orders/42416"
      }
    ],
    "collection": [
      {
        "href": "https://caraluzzis.com/wp-json/wc/v3/orders"
      }
    ]
  }
}}


item_name = ""
item_qty = int
item_mods = []

itemlist = []
sub_item_list = []

first = input_data["data"]["billing"]["first_name"]
last = input_data["data"]["billing"]["last_name"]
phone = input_data["data"]["billing"]["phone"]
cart_hash = input_data["data"]["cart_hash"]
placed_time = input_data["data"]["date_paid"]
customer_note = input_data["data"]["customer_note"]
name = f"{first} {last}"


deli_order = {
  "id": cart_hash,
  "name": name,
  "time": placed_time,
  "pickupTime": "",
  "phoneNumber": phone,
  "mode": "",
  "items": itemlist,
  "terminal": "Deli",
  "specialInstructions": customer_note,


}

sub_order = {
    "id": f"{cart_hash}_sub_order",
    "name": name,
    "time": placed_time,
    "pickupTime": "",
    "phoneNumber": phone,
    "mode": "",
    "items": sub_item_list,
    "terminal": "Sub Shop",
    "specialInstructions": customer_note,
}

i = 0

for item in input_data["data"]["line_items"]:
    modlist = []
    
    plu = input_data["data"]["line_items"][0]["sku"]
    send_item = {

      "id": "",
      "name": "",
      "qty": "",
      "mods": modlist

    }
    
    if item.get("meta_data")[0].get("value") == "Slice":
        plu = input_data["data"]["line_items"][i]["sku"]
        send_item["id"] = plu

        item_name = item.get("name")
        send_item["name"] = item_name
        
        item_qty = item.get("quantity")
        send_item["qty"] = item_qty

        myval = item.get("meta_data")[0].get("value")
        sliceorweight = item.get("meta_data")[1].get("value")
        thickness = item.get("meta_data")[2].get("value")
        modlist.append(myval)
        modlist.append(sliceorweight)
        modlist.append(thickness)

        itemlist.append(send_item)
        i += 1

    elif item.get("meta_data")[0].get("value") == "Weight":
        plu = input_data["data"]["line_items"][i]["sku"]
        send_item["id"] = plu

        item_name = item.get("name")
        send_item["name"] = item_name

        item_qty = item.get("quantity")
        send_item["qty"] = item_qty

        myval = item.get("meta_data")[0].get("value")
        sliceorweight = item.get("meta_data")[1].get("value")
        thickness = item.get("meta_data")[2].get("value")
        modlist.append(myval)
        modlist.append(sliceorweight)
        modlist.append(thickness)

        itemlist.append(send_item)
        i += 1

    else:
        plu = input_data["data"]["line_items"][i]["sku"]
        send_item["id"] = plu

        item_name = item.get("name")
        send_item["name"] = item_name

        item_qty = item.get("quantity")
        send_item["qty"] = item_qty

        sub_val = item.get("meta_data")[0].get("value")
        modlist.append(sub_val)

        sub_item_list.append(send_item)
        i += 1

if len(sub_order["items"]) >= 1:
    output = {"deli_order": deli_order, "sub_order": sub_order}
else:
    output = {"deli_order": deli_order}
newout = json.dumps(output)
print(newout)

