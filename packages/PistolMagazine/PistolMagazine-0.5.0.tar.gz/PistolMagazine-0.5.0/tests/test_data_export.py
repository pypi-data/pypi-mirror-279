from pistol_magazine.data_exporter import CSVExporter, JSONExporter, XMLExporter, DBExporter

data = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "Los Angeles"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]


data_xml = {
    "users": [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com",
            "profile": {
                "age": 30,
                "city": "New York"
            }
        },
        {
            "id": 2,
            "name": "Bob",
            "email": "bob@example.com",
            "profile": {
                "age": 25,
                "city": "Los Angeles"
            }
        }
    ]
}


def test():
    # Export to CSV
    csv_exporter = CSVExporter()
    csv_exporter.export(data, 'output.csv')

    # Export to JSON
    json_exporter = JSONExporter()
    json_exporter.export(data, 'output.json')

    # Export to XML
    xml_exporter = XMLExporter()
    xml_exporter.export(data_xml, 'output.xml')


# # Export to MySQL Database
# db_exporter = DBExporter(table_name='persons')
# db_exporter.export(data)
