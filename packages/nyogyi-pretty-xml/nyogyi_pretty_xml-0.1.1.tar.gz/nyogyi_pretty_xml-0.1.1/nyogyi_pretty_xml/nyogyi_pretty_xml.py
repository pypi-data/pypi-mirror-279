import argparse
from lxml import etree
import time

def pretty_print_xml(input_file, output_file):
    # Measure start time
    start_time = time.time()
    
    # Parse the XML file
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(input_file, parser)
    
    # Pretty print the XML
    pretty_xml = etree.tostring(tree, pretty_print=True, encoding='utf-8')
    
    # Write the pretty printed XML to the output file
    with open(output_file, 'wb') as f:
        f.write(pretty_xml)
    
    # Measure end time
    end_time = time.time()
    print(f"Pretty printed XML saved to {output_file}. Time taken: {end_time - start_time:.2f} seconds")

def main():
    parser = argparse.ArgumentParser(description="Pretty print an XML file.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input XML file")
    parser.add_argument('-o', '--output', required=True, help="Path to the output XML file")

    args = parser.parse_args()

    pretty_print_xml(args.input, args.output)

if __name__ == "__main__":
    main()
