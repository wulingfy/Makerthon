import xml.etree.ElementTree as ET
import json
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

if __name__ == "__main__":
    result = get_data_pronunciation()
    for cons in result:
        print("Content:", cons['content'])
        print("Accuracy Score:", cons['accuracy_score'])
        print("Fluency Score:", cons['fluency_score'])
        print("Standard Score:", cons['standard_score'])
        print("Total Score:", cons['total_score'])
        print('\n')
    
    