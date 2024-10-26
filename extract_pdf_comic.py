import fitz  # PyMuPDF
import os

def extract_raw_images_from_directory(input_directory, output_directory):
    # 检查输出目录是否存在，如果不存在，则创建它
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 遍历指定目录中的所有文件
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(input_directory, file_name)
            doc = fitz.open(pdf_path)

            # 创建以PDF文件名命名的子文件夹
            pdf_folder_name = os.path.splitext(file_name)[0]  # 移除.pdf扩展名
            pdf_output_path = os.path.join(output_directory, pdf_folder_name)
            if not os.path.exists(pdf_output_path):
                os.makedirs(pdf_output_path)

            # 处理每一页的图片
            for i in range(len(doc)):
                for img_index, img in enumerate(doc.get_page_images(i)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]  # 获取原始图片数据
                    image_ext = base_image["ext"]      # 图片格式
                    image_filename = f"page_{i}_img_{img_index}.{image_ext}"
                    image_full_path = os.path.join(pdf_output_path, image_filename)
                    with open(image_full_path, 'wb') as img_file:
                        img_file.write(image_bytes)
                    print(f"Extracted {image_full_path}")

# 输入和输出目录
input_directory = r"temp\comic\original"
output_directory = r"temp\comic\extract"
extract_raw_images_from_directory(input_directory, output_directory)