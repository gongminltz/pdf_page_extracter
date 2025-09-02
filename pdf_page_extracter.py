import os
import argparse
from PyPDF2 import PdfReader, PdfWriter

"""
使用示例：
python pdf_page_extracter.py example.pdf extracted_pages.pdf "1-3,5,7-9"
"""


def parse_page_range(page_range):
    """
    解析页面范围字符串，返回页面索引列表
    :param page_range: 页面范围字符串，例如 "1-3" 或 "1,3,5"
    :return: 页面索引列表
    """
    page_indices = []
    for part in page_range.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            page_indices.extend(range(start - 1, end))  # 转换为从 0 开始的索引
        else:
            page_indices.append(int(part) - 1)  # 转换为从 0 开始的索引
    return sorted(set(page_indices))  # 去重并排序


def extract_pages(input_file, output_file, pages_to_extract):
    """
    提取 PDF 文件中指定的若干页面
    :param input_file: 输入的 PDF 文件路径
    :param output_file: 输出的 PDF 文件路径
    :param pages_to_extract: 要提取的页面索引列表（从 0 开始）
    """
    if not os.path.exists(input_file):
        print(f"文件 {input_file} 不存在")
        return

    pdf_reader = PdfReader(input_file)
    pdf_writer = PdfWriter()

    for page_num in pages_to_extract:
        if 0 <= page_num < len(pdf_reader.pages):
            pdf_writer.add_page(pdf_reader.pages[page_num])
        else:
            print(f"页面 {page_num + 1} 超出 PDF 文件的页码范围")

    with open(output_file, "wb") as out:
        pdf_writer.write(out)

    print(f"已成功提取指定页面到 {output_file}")

def main():
    parser = argparse.ArgumentParser(description="提取 PDF 文件中指定的若干页面")
    parser.add_argument("input_file", type=str, help="输入的 PDF 文件路径")
    parser.add_argument("output_file", type=str, help="输出的 PDF 文件路径")
    parser.add_argument("pages_to_extract", type=str, help="要提取的页面范围，例如 '1-3' 或 '1,3,5'")
    args = parser.parse_args()

    pages_to_extract = parse_page_range(args.pages_to_extract)
    extract_pages(args.input_file, args.output_file, pages_to_extract)

if __name__ == "__main__":
    main()