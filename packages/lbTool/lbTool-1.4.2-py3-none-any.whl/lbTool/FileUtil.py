import PyPDF2
import comtypes.client


def merge_pdf(input_files, output_file):
    """
    合并pdf
    :param input_files: 待合并文件路径列表（合并顺序依次排列）
    :param output_file: 保存文件路径
    :return:
    """
    merger = PyPDF2.PdfMerger()

    for pdf in input_files:
        with open(pdf, 'rb') as file:
            merger.append(file)

    with open(output_file, 'wb') as output:
        merger.write(output)


def save_file(binary_stream, output_file, mode):
    """
    文件流保存文件
    :param binary_stream: 数据流
    :param output_file: 保存文件路径
    :param mode: 文件操作方式 w|wb|a|ab
    :return:
    """
    with open(output_file, mode) as file:
        file.write(binary_stream)


def word_to_pdf(input_file, output_file, remove_header=True, remove_footer=True):
    """
    word文档转pdf
    :param input_file: word文档路径
    :param output_file: pdf保存路径
    :param remove_header: 是否移除word文档中的页眉
    :param remove_footer: 是否移除word文档中的页脚
    :return:
    """
    # 初始化 Word 应用程序
    word = comtypes.client.CreateObject("Word.Application")
    try:
        # 打开 Word 文档
        doc = word.Documents.Open(input_file, NoEncodingDialog=True)
        # 设置页面边距（单位为磅，1 英寸 = 72 磅）
        # doc.PageSetup.LeftMargin = 36
        # doc.PageSetup.RightMargin = 36
        # doc.PageSetup.TopMargin = 36
        # doc.PageSetup.BottomMargin = 36

        if remove_header is True:
            # 清空所有节（Sections）的页眉内容
            for section in doc.Sections:
                section.Headers(1).Range.Text = ""

        if remove_footer is True:
            # 清空所有节（Sections）的页脚内容
            for section in doc.Sections:
                section.Footers(1).Range.Text = ""

        # 将文档保存为 PDF
        doc.SaveAs(output_file, FileFormat=17)  # 17 表示 PDF 格式

        # 关闭文档和 Word 应用程序
        doc.Close()
        # word.Quit()
    except Exception as e:
        print(f"Error: {e}")
        raise Exception(e)
    finally:
        word.Quit()
