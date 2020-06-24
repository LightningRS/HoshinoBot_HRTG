#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
class Text2Img(object):
    """
    将文本消息转换成图片
    """
    def __init__(self, text):
        self.text: str = text
        self.res_width = 500
        self.line_space = 5
        self.font_size = 20
        self.padding = 20
        self.font = ImageFont.truetype("simhei.ttf", self.font_size)
    
    def set_font(self, fontfile: str, fontsize: int):
        self.font_size = fontsize
        self.font = ImageFont.truetype(fontfile, self.font_size)

    def _split_p(self, p_text):
        img_tmp = Image.new('RGBA', (150, 150), (255, 255, 255, 0))
        draw_tmp = ImageDraw.Draw(img_tmp)
        res_buffer = ""
        res = list()
        sum_width = 0
        line_cnt = 1
        sum_height = 0
        max_line_height = 0
        max_line_width = 0

        # 取空格高度
        bl_width, bl_height = draw_tmp.textsize(' ', self.font)
        # 遍历字符
        for ch in p_text:
            ch_width, ch_height = draw_tmp.textsize(ch, self.font)
            sum_width += ch_width
            if sum_width > (self.res_width - self.padding * 2):
                line_cnt += 1
                max_line_width = max(max_line_width, sum_width)
                sum_width = 0
                line_height = max_line_height + self.line_space
                sum_height += line_height
                max_line_height = 0
                res.append((res_buffer, line_height))
                res_buffer = ''
            res_buffer += ch
            # if ch_height > max_line_height:
                # print("higher character: %s, %d" % (ch, ch_height))
            max_line_height = max(max_line_height, ch_height)

        max_line_width = max(max_line_width, sum_width)

        if not res_buffer.endswith('\n'):
            line_height = max(max_line_height, bl_height) + self.line_space
            res.append((res_buffer, line_height))
            sum_height += line_height
        return res, sum_height, line_cnt, max_line_width

    def split_text(self):
        # 按换行符分段
        pg = self.text.split('\n')
        sum_height = 0
        sum_lines = 0
        all_text = list()
        max_width = 0
        for p in pg:
            p_res, p_sumh, p_linecnt, p_maxw = self._split_p(p)
            max_width = max(max_width, p_maxw)
            sum_height += p_sumh
            sum_lines += p_linecnt
            all_text.extend(p_res)
        return all_text, sum_height, max_width
    
    def get_img(self):
        all_text, res_height, max_line_width = self.split_text()
        res_img = Image.new('RGBA', (max_line_width + (self.padding * 2), res_height + (self.padding * 2)), (255, 255, 255, 255))
        res_draw = ImageDraw.Draw(res_img)
        x, y = self.padding, self.padding
        for text, lineh in all_text:
            # print((text, lineh))
            res_draw.text((x, y), text, fill=(0, 0, 0), font=self.font)
            y += lineh
        return res_img

if __name__ == '__main__':
    text = """
        测试转换结果行 1
        测试转换结果行 2
    """
    t2i = Text2Img(text)
    t2i.get_img().save("result.png")
