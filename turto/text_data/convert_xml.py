import xml.etree.ElementTree as ET
import json
import csv
# Đọc file XML
tree = ET.parse('text_data/assessment-point.xml')  # Thay 'your_file.xml' bằng đường dẫn tới file XML của bạn
root = tree.getroot()

# Duyệt qua các phần tử và lưu các giá trị score vào dictionary
def get_data_pronunciation():
    data = []
    for read_sentence in root.findall('read_sentence'):
        for rec_paper in read_sentence.findall('rec_paper'):
            for read_chapter in rec_paper.findall('read_chapter'):
                chapter_data = {
                    'content': read_chapter.attrib.get('content'),
                    'sentences': [] 
                }
                for sentence in read_chapter.findall('sentence'):
                    sentence_data = {
                        'content': sentence.attrib.get('content'),
                        'accuracy_score': sentence.attrib.get('accuracy_score'),
                        'fluency_score': sentence.attrib.get('fluency_score'),
                        'standard_score': sentence.attrib.get('standard_score'),
                        'total_score': sentence.attrib.get('total_score'),
                    }
                    data.append(sentence_data)
    return data
    
def append_data():
    result = get_data_pronunciation()
    headers = ["Content", "Accuracy Score", "Fluency Score", "Standard Score", "Total Score"]
    with open('text_data/data_pronunciation.csv', mode='a', newline='', encoding='utf-8') as file:
        file.seek(0, 2)  # Move the file pointer to the end
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header only if the file is empty
        # Check if the file is empty by trying to read the first line
    
        if file.tell() == 0:  # If the file is empty
            writer.writeheader()
        # Write the data rows
        for cons in result:
            print(cons)
            writer.writerow({
                "Content": cons['content'],
                "Accuracy Score": cons['accuracy_score'],
                "Fluency Score": cons['fluency_score'],
                "Standard Score": cons['standard_score'],
                "Total Score": cons['total_score']
            })