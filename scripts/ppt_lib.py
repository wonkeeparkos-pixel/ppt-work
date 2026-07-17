# -*- coding: utf-8 -*-
"""공유 PPT 라이브러리 — 슬라이드 템플릿 기반 덱 생성기."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

NAVY  = RGBColor(0x1B,0x35,0x5E); NAVY2 = RGBColor(0x24,0x47,0x74)
TEAL  = RGBColor(0x2C,0x89,0x8A); TEALD = RGBColor(0x1F,0x6E,0x70)
INK   = RGBColor(0x1A,0x20,0x2C); MUTE  = RGBColor(0x5A,0x6B,0x7B)
LGRAY = RGBColor(0xEE,0xF2,0xF6); CARD  = RGBColor(0xF5,0xF8,0xFB)
WHITE = RGBColor(0xFF,0xFF,0xFF); GREEN = RGBColor(0x2E,0x7D,0x32)
AMBER = RGBColor(0xB9,0x7A,0x0C); RED   = RGBColor(0xB0,0x3A,0x2E)
LINE  = RGBColor(0xD5,0xDE,0xE7); ICE   = RGBColor(0xBF,0xD3,0xE6)
MINT  = RGBColor(0x9F,0xE0,0xD8)
FONT = "NanumGothic"

class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333); self.prs.slide_height = Inches(7.5)
        self.BLANK = self.prs.slide_layouts[6]
        self.SW = self.prs.slide_width; self.SH = self.prs.slide_height

    def _slide(self):
        return self.prs.slides.add_slide(self.BLANK)

    def _f(self, run, size, color, bold=False, italic=False):
        run.font.size=Pt(size); run.font.color.rgb=color; run.font.bold=bold
        run.font.italic=italic; run.font.name=FONT
        rPr=run._r.get_or_add_rPr(); ea=rPr.find(qn('a:ea'))
        if ea is None: ea=rPr.makeelement(qn('a:ea'),{}); rPr.append(ea)
        ea.set('typeface',FONT)

    def rect(self,s,x,y,w,h,fill,line=None,lw=0.75,round_=False):
        shp=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,x,y,w,h)
        if round_:
            try: shp.adjustments[0]=0.08
            except Exception: pass
        if fill is None: shp.fill.background()
        else: shp.fill.solid(); shp.fill.fore_color.rgb=fill
        if line is None: shp.line.fill.background()
        else: shp.line.color.rgb=line; shp.line.width=Pt(lw)
        shp.shadow.inherit=False; return shp

    def text(self,s,x,y,w,h,paras,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,after=4,ls=1.08,wrap=True):
        tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=wrap; tf.vertical_anchor=anchor
        tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
        for i,para in enumerate(paras):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
            p.alignment=align; p.space_after=Pt(after); p.line_spacing=ls
            for it in para:
                r=p.add_run(); r.text=it[0]
                self._f(r,it[1],it[2],it[3] if len(it)>3 else False,it[4] if len(it)>4 else False)
        return tb

    def card(self,s,x,y,w,h,fill=CARD,line=LINE):
        return self.rect(s,x,y,w,h,fill,line=line,lw=1.0,round_=True)

    def header(self,s,title,eyebrow=None,tag=None,tag_color=TEAL):
        self.rect(s,Inches(0.55),Inches(0.34),Inches(0.12),Inches(0.5),TEAL)
        self.text(s,Inches(0.8),Inches(0.26),Inches(10.4),Inches(0.75),[[(title,24,NAVY,True)]],anchor=MSO_ANCHOR.MIDDLE)
        if eyebrow:
            self.text(s,Inches(0.82),Inches(0.12),Inches(8),Inches(0.24),[[(eyebrow,11,TEALD,True)]])
        self.rect(s,Inches(0.8),Inches(1.06),Inches(11.9),Pt(1.4),LINE)
        if tag:
            w=Inches(0.3+0.12*len(tag))
            self.rect(s,self.SW-w-Inches(0.55),Inches(0.4),w,Inches(0.38),tag_color,round_=True)
            self.text(s,self.SW-w-Inches(0.55),Inches(0.4),w,Inches(0.38),[[(tag,11.5,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)

    def footer(self,s,src):
        page=len(self.prs.slides._sldIdLst)
        self.text(s,Inches(0.8),Inches(7.06),Inches(10.8),Inches(0.32),[[("근거: "+src,9,MUTE)]],anchor=MSO_ANCHOR.MIDDLE)
        self.text(s,Inches(12.1),Inches(7.06),Inches(0.9),Inches(0.32),[[(str(page),10,MUTE,True)]],align=PP_ALIGN.RIGHT,anchor=MSO_ANCHOR.MIDDLE)

    def bullets(self,s,x,y,w,h,items,size=15,gap=7):
        tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
        tf.margin_left=0;tf.margin_right=0;tf.margin_top=0;tf.margin_bottom=0
        for i,it in enumerate(items):
            lv=it[0]; tx=it[1]; c=it[2] if len(it)>2 and it[2] else INK; b=it[3] if len(it)>3 else False
            sz=it[4] if len(it)>4 else size
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
            p.space_after=Pt(gap); p.line_spacing=1.08; p.alignment=PP_ALIGN.LEFT
            mark="" if lv<0 else ("●  " if lv==0 else "–  ")
            indent="" if lv<=0 else ("      "*lv)
            r=p.add_run(); r.text=indent+mark; self._f(r,sz*0.7 if lv==0 else sz,TEAL if lv==0 else MUTE,True)
            r2=p.add_run(); r2.text=tx; self._f(r2,sz,c,b)
        return tb

    def table(self,s,x,y,w,rows,col_w,size=12,row_h=Inches(0.5),head=12.5,zebra=True):
        n=len(rows); nc=len(col_w); total=sum(col_w,Emu(0))
        gt=s.shapes.add_table(n,nc,x,y,total,row_h*n).table
        gt.first_row=False; gt.horz_banding=False
        for ci,cw in enumerate(col_w): gt.columns[ci].width=cw
        for ri,row in enumerate(rows):
            gt.rows[ri].height=Inches(0.5) if ri==0 else row_h
            for ci,val in enumerate(row):
                cell=gt.cell(ri,ci); cell.margin_left=Inches(0.08); cell.margin_right=Inches(0.06)
                cell.margin_top=Inches(0.02); cell.margin_bottom=Inches(0.02); cell.vertical_anchor=MSO_ANCHOR.MIDDLE
                if ri==0: cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
                else: cell.fill.solid(); cell.fill.fore_color.rgb=WHITE if (not zebra or ri%2==1) else LGRAY
                tf=cell.text_frame; tf.word_wrap=True; p=tf.paragraphs[0]
                p.alignment=PP_ALIGN.LEFT if ci==0 else PP_ALIGN.CENTER
                txt=val[0] if isinstance(val,tuple) else val
                col=val[1] if isinstance(val,tuple) else (WHITE if ri==0 else INK)
                bold=val[2] if (isinstance(val,tuple) and len(val)>2) else (ri==0)
                r=p.add_run(); r.text=txt; self._f(r,head if ri==0 else size,col,bold)
        return gt

    # ---------------- templates ----------------
    def title_slide(self,eyebrow,title_lines,subtitle,order,note):
        s=self._slide()
        self.rect(s,0,0,self.SW,self.SH,WHITE)
        self.rect(s,0,0,self.SW,Inches(4.55),NAVY)
        self.rect(s,0,Inches(4.55),self.SW,Inches(0.09),TEAL)
        self.rect(s,0,0,Inches(0.22),Inches(4.55),TEAL)
        self.text(s,Inches(0.9),Inches(1.0),Inches(11.5),Inches(0.4),[[(eyebrow,15,ICE,True)]])
        self.text(s,Inches(0.9),Inches(1.5),Inches(11.6),Inches(2.0),[[(t,32,WHITE,True)] for t in title_lines],ls=1.12)
        self.text(s,Inches(0.9),Inches(3.5),Inches(11.5),Inches(0.55),[[(subtitle,13,RGBColor(0xAF,0xC6,0xDF),False,True)]])
        self.text(s,Inches(0.9),Inches(4.95),Inches(11.5),Inches(1.1),[[(order,13.5,INK,True)]],after=6)
        self.text(s,Inches(0.9),Inches(6.62),Inches(11.5),Inches(0.5),[[(note,11,MUTE,False,True)]])
        return s

    def bullets_slide(self,title,eyebrow,tag,items,footer,tag_color=TEAL,size=15,gap=9):
        s=self._slide(); self.header(s,title,eyebrow,tag,tag_color)
        self.bullets(s,Inches(0.8),Inches(1.5),Inches(11.85),Inches(5.2),items,size=size,gap=gap)
        self.footer(s,footer); return s

    def split_slide(self,title,eyebrow,tag,left,card_spec,footer,tag_color=TEAL,dark_card=False):
        s=self._slide(); self.header(s,title,eyebrow,tag,tag_color)
        self.bullets(s,Inches(0.8),Inches(1.5),Inches(7.0),Inches(5.1),left,size=14,gap=8)
        ct,citems,ccolor=card_spec
        fill=NAVY if dark_card else CARD
        self.card(s,Inches(8.1),Inches(1.6),Inches(4.5),Inches(4.9),fill,line=None if dark_card else LINE)
        self.text(s,Inches(8.4),Inches(1.85),Inches(4.0),Inches(0.4),[[(ct,13,ICE if dark_card else TEALD,True)]])
        norm=[]
        for it in citems:
            lv=it[0]; tx=it[1]; c=it[2] if len(it)>2 and it[2] else (WHITE if dark_card else INK)
            b=it[3] if len(it)>3 else False
            norm.append((lv,tx,c,b))
        self.bullets(s,Inches(8.4),Inches(2.4),Inches(3.95),Inches(4.0),norm,size=12.5,gap=8)
        self.footer(s,footer); return s

    def table_slide(self,title,eyebrow,tag,rows,col_w,footer,tag_color=TEAL,size=12,row_h=Inches(0.5),note=None):
        s=self._slide(); self.header(s,title,eyebrow,tag,tag_color)
        self.table(s,Inches(0.8),Inches(1.5),Inches(11.85),rows,col_w,size=size,row_h=row_h)
        if note:
            self.text(s,Inches(0.8),Inches(6.55),Inches(11.8),Inches(0.4),[[(note,11.5,TEALD,True)]])
        self.footer(s,footer); return s

    def key_slide(self,eyebrow,headline,msgs):
        s=self._slide()
        self.rect(s,0,0,self.SW,self.SH,NAVY); self.rect(s,0,0,Inches(0.22),self.SH,TEAL)
        self.text(s,Inches(0.9),Inches(0.7),Inches(11.5),Inches(0.5),[[(eyebrow,13,MINT,True)]])
        self.text(s,Inches(0.9),Inches(1.2),Inches(11.5),Inches(1.0),[[(headline,22,WHITE,True)]],ls=1.1)
        n=len(msgs); top=2.5; step=min(0.95,(6.6-top)/n)
        for i,(t,d) in enumerate(msgs):
            y=Inches(top+i*step)
            self.rect(s,Inches(0.9),y+Inches(0.04),Inches(0.16),Inches(step*0.66*72/72*0.9),TEAL)
            self.text(s,Inches(1.25),y,Inches(3.2),Inches(step*0.9),[[(t,14,MINT,True)]],anchor=MSO_ANCHOR.MIDDLE)
            self.text(s,Inches(4.5),y,Inches(8.1),Inches(step*0.9),[[(d,12.5,WHITE)]],anchor=MSO_ANCHOR.MIDDLE,ls=1.05)
        return s

    def refs_slide(self,title,refs):
        s=self._slide(); self.header(s,title,eyebrow="참고문헌",tag="References")
        half=(len(refs)+1)//2
        for col,chunk in enumerate([refs[:half],refs[half:]]):
            x=Inches(0.8+col*6.0)
            self.text(s,x,Inches(1.5),Inches(5.75),Inches(5.3),[[(r,10,INK)] for r in chunk],after=7,ls=1.05)
        self.footer(s,"PubMed/저널 목록 대조 — 조작 인용 없음"); return s

    def save(self,path):
        self.prs.save(path); return len(self.prs.slides._sldIdLst)
