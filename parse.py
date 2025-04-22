import xml.etree.ElementTree as ET

# Load XML from file
with open("text_data/assessment-point.xml", "r", encoding="utf-8") as f:
    xml_content = f.read()

# Parse the XML
root = ET.fromstring(xml_content)

# Output file
output_filename = "text_data/sentence_report.txt"
# Write to txt file
with open(output_filename, "w", encoding="utf-8") as out_file:
    # Header
    out_file.write("accuracy_score\tfluency_score\tstandard_score\tindex\ttotal_score\tstruct\tword_count\n")

    # Find all sentence elements
    for sentence in root.findall(".//sentence"):
        accuracy = sentence.get("accuracy_score", "")
        fluency = sentence.get("fluency_score", "")
        standard = sentence.get("standard_score", "")
        index = sentence.get("index", "")
        total = sentence.get("total_score", "")
        word_count = sentence.get("word_count", "")

        # Struct is hidden (empty string or any placeholder)
        struct = ""

        # Write row
        # PARSE ĐƠN GIẢN CÁC THÔNG TIN TRONG FILE ĐIỂM ASSESSMENT-POINT.XML
        out_file.write(f"{accuracy}\t{fluency}\t{standard}\t{index}\t{total}\t{struct}\t{word_count}\n")

print(f"Done! Output saved to {output_filename}")
