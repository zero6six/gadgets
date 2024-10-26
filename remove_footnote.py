import re

def remove_wikipedia_references(text):
    # 使用正则表达式来匹配方括号中的数字（即类似[1], [2]等）
    cleaned_text = re.sub(r'\[\d+\]', '', text)
    return cleaned_text

# 示例文本
wikipedia_text = """
"""

# 去除注释后的文本
cleaned_text = remove_wikipedia_references(wikipedia_text)

with open("temp/output.txt", 'w', encoding='utf-8') as f:
    f.write(cleaned_text)
