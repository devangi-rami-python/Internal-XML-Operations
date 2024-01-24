import csv
import xml.etree.ElementTree as ET

def xml_to_csv(xml_file, csv_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(csv_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header row
        header = []
        for child in root[0]:
            print('child: ', child.tag)
            header.append(child.tag)
        csv_writer.writerow(header)

        # Write data rows
        for element in root:
            row = []
            for child in element:
                row.append(child.text)
            csv_writer.writerow(row)

        # Write header to CSV using XML tags
        # header_written = False
        # for element in root.iter():
        #     print('element: ', element)
        #     if not header_written:
        #         csv_writer.writerow([element.tag])
        #         header_written = True

        #     # Iterate through each child element
        #     for child in element:
        #         child_tag = child.tag
        #         # print('child_tag: ', child_tag)
        #         child_text = child.text.strip() if child.text is not None else ""

        #         # Write data to CSV
        #         csv_writer.writerow([child_text])

            # Open CSV file for writing
        # with open(csv_file, 'w', newline='') as csvfile:
        #     csv_writer = csv.writer(csvfile)

        #     # Write header to CSV using XML tags without namespace
        #     header_written = False
        #     for element in root.iter():
        #         if not header_written:
        #             csv_writer.writerow([element.tag.split('}')[1] if '}' in element.tag else element.tag])
        #             header_written = True

        #         # Iterate through each child element
        #         for child in element:
        #             child_tag = child.tag.split('}')[1] if '}' in child.tag else child.tag
        #             child_text = child.text.strip() if child.text is not None else ""

        #             # Write data to CSV
        #             csv_writer.writerow([child_text])

if __name__ == "__main__":
    xml_file = "main.xml"
    csv_file = "your_output.csv"
    xml_to_csv(xml_file, csv_file)
