import pyecharts.options as opts
from pyecharts.charts import Line, Grid


from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
from PIL import Image

## this process is noly for chorme driver. maybe, you should use Windows.

def visual_data_by_line_bar(x_data, y_data_1, y_data_2, y_data_3, y_data_4, out_dir=None, issave_pdf=True):
    try:
        from snapshot_selenium import snapshot as driver

    except:
        print("please install requirement/addition.txt")
    # # 6194, 
    # def line_chart() -> Line:
    #     c = (
    #         Line(init_opts=opts.InitOpts(width="400px", bg_color="white", height="300px"))
    #         .set_global_opts(
    #             tooltip_opts=opts.TooltipOpts(is_show=False),
    #             xaxis_opts=opts.AxisOpts(
    #                 type_="category",
    #                 axistick_opts=opts.AxisTickOpts(is_show=True),
    #                 splitline_opts=opts.SplitLineOpts(is_show=False),
    #                 axislabel_opts=opts.LabelOpts(color="black", interval="0", rotate=-90, font_size=12, font_weight="bold", text_width=200, text_height=200),
    #                 name = "Predicate",
    #                 name_location = "middle",
    #                 name_gap = 100,
    #                 name_textstyle_opts = opts.TextStyleOpts(color="black", font_size=20, font_weight="bold"),
    #                 # boundary_gap= ['30%', '30%']
    #                 # axislabel_opts = opts.LabelOpts(),boundaryGap: ['20%', '20%']
    #             ),
    #             yaxis_opts=opts.AxisOpts(
    #                 type_="value",
    #                 min_ = 0,
    #                 max_ = 1,
    #                 name = "Recall@100",
    #                 name_location = "middle",
    #                 name_gap = 50,
    #                 name_textstyle_opts = opts.TextStyleOpts(color="black", font_size=20, font_weight="bold"),
    #                 axisline_opts=opts.AxisLineOpts(is_show=True),
    #                 axistick_opts=opts.AxisTickOpts(is_show=True),
    #                 splitline_opts=opts.SplitLineOpts(is_show=True),
    #                 axislabel_opts = opts.LabelOpts(color="black", font_size=12, font_weight="bold", text_height=100),
    #             ),
    #         )
    #         .add_xaxis(
    #             xaxis_data=x_data,
    #         )
    #         .add_yaxis(
    #             series_name="2 blocks",
    #             y_axis=y_data_1,
    #             symbol="emptyCircle",
    #             is_symbol_show=True,
    #             label_opts=opts.LabelOpts(is_show=False),
    #         )
    #         .add_yaxis(
    #             series_name="1 block",
    #             y_axis=y_data_2,
    #             symbol="rect",
    #             is_symbol_show=True,
    #             label_opts=opts.LabelOpts(is_show=False),
    #         )
    #         # .render("basic_line_chart.html")
    #     )
    #     return c

    bar = (
        Bar(init_opts=opts.InitOpts(bg_color="white"))
        .add_xaxis(x_data)
        .add_yaxis(
            "",
            y_data_3,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(opacity=0.3),
            color="blue",
        )
        .add_yaxis(
            "",
            y_data_4,
            yaxis_index=1,
            label_opts=opts.LabelOpts(is_show=False),
            itemstyle_opts=opts.ItemStyleOpts(opacity=0.3),
            color="#FF99CC",
        )
    )

    line = (
        Line(init_opts=opts.InitOpts(bg_color="white"))
        .add_xaxis(x_data)
        .add_yaxis(
            "2 blocks",
            y_data_1,
            color="blue",
            label_opts=opts.LabelOpts(is_show=False),
            symbol="emptyCircle",
        )
        .add_yaxis(
            "1 block",
            y_data_2,
            color="#FF99CC",
            label_opts=opts.LabelOpts(is_show=False),
            symbol="rect",
            symbol_size=5,
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                interval=100,
                name="Frequency",
                name_location = "middle",
                name_gap = 50,
                min_=0,
                max_=500,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    is_show=True
                ),
                name_textstyle_opts = opts.TextStyleOpts(color="black", font_size=20),
                axislabel_opts = opts.LabelOpts(color="black",  font_size=12, font_weight="bold", text_height=100),
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=False),
            legend_opts=opts.LegendOpts(
                pos_top="5px",
                pos_left="center",
                orient="horizontal",
                item_gap=10,
                textstyle_opts=opts.TextStyleOpts(font_size=10),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(color="black", interval="0", rotate=45, font_weight="bold", font_size=10, text_width=200, text_height=200),
                name = "Predicate",
                name_location = "middle",
                name_gap = 100,
                name_textstyle_opts = opts.TextStyleOpts(color="black", font_size=20),
                boundary_gap= ['10%', '10%']
            ),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                position="right",
                min_ = 0.2,
                max_ = 0.7,
                name = "Recall@100",
                name_location = "middle",
                name_gap = 50,
                name_textstyle_opts = opts.TextStyleOpts(color="black", font_size=20),
                axisline_opts=opts.AxisLineOpts(is_show=True),
                axislabel_opts = opts.LabelOpts(color="black", font_size=12, font_weight="bold", text_height=100),
            ),
        )
    )

    overlap_1 = line.overlap(bar)


    grid = (
        Grid(init_opts=opts.InitOpts(width="400px", height="270px", bg_color="white"))
        .add(
            overlap_1, grid_opts=opts.GridOpts(pos_top="30px",pos_bottom="70px"), is_control_axis_index=True
        )
    )

    if out_dir is None:
        out_dir = "result.jpg"
    # grid.render()
    # 需要安装 snapshot-selenium 或者 snapshot-phantomjs
    make_snapshot(driver, grid.render(), out_dir)
    
    if issave_pdf:
        chart_image = Image.open(out_dir)
        chart_width, chart_height = chart_image.size

        # 根据图表大小设置PDF页面大小
        # 注意：reportlab使用点(pt)作为单位，1英寸 = 72pt
        pdf_width = chart_width * 72 / 96  # 将像素转换为点
        pdf_height = chart_height * 72 / 96  # 将像素转换为点

        # 创建PDF文件
        pdf_file = out_dir.split('.')[0] + ".pdf"
        c = canvas.Canvas(pdf_file, pagesize=(pdf_width, pdf_height))

        # 将图表图片添加到PDF文件中
        c.drawImage(out_dir, x=0, y=0, width=pdf_width, height=pdf_height, preserveAspectRatio=True)

        # 保存并关闭PDF文件
        c.save()


if __name__ == "__main__":
        
    x_data = [
        'over',
        'in front of',
        'beside',
        'on',
        'in',
        'attached to',
        'hanging from',
        'on back of',
        'falling off',
        'going down',
        'painted on',
        'walking on',
        'running on',
        'crossing',
        'standing on',
        'lying on',
        'sitting on',
        'flying over',
        'jumping over',
        'jumping from',
        'wearing',
        'holding',
        'carrying',
        'looking at',
        'guiding',
        'kissing',
        'eating',
        'drinking',
        'feeding',
        'biting',
        'catching',
        'picking',
        'playing with',
        'chasing',
        'climbing',
        'cleaning',
        'playing',
        'touching',
        'pushing',
        'pulling',
        'opening',
        'cooking',
        'talking to',
        'throwing',
        'slicing',
        'driving',
        'riding',
        'parked on',
        'driving on',
        'about to hit',
        'kicking',
        'swinging',
        'entering',
        'exiting',
        'enclosing',
        'leaning on',
    ]
    # [0] * 56

    y_data_1 =  [0.5925413302575933, 0.4567951713395638, 0.4501617280444318, 0.4296761229116412, 0.3694455498076668, 0.41633855331841907, 0.3907563025210084, 0.23076923076923078, 0.6666666666666666, 0.3333333333333333, 0.0, 0.5792792792792794, 0.5863678804855276, 0.42857142857142855, 0.613162563761366, 0.48122065727699526, 0.509963768115942, 0.49358974358974356, 0.5, 0.5555555555555556, 0.4522357723577235, 0.5831168831168831, 0.36970899470899465, 0.5383522727272727, 0.07692307692307693, 0.0, 0.5467836257309941, 0.42857142857142855, 0.4444444444444444, 0.5, 0.5333333333333333, 0.0, 0.421875, 0.4166666666666667, 0.0, 0.14285714285714285, 0.6942666666666667, 0.47058823529411764, 0.16666666666666666, 0.3409090909090909, 0.0, 0.2, 0.37719298245614036, 0.9166666666666666, 0.5, 0.2441860465116279, 0.731159420289855, 0.42770034843205573, 0.5817708333333333, 0.7777777777777778, 0.75, 0.8552631578947368, 0.22727272727272727, 0.0, 0.22404371584699453, 0.17261904761904762]
    # y_data_2 =  [0.5295847750865051, 0.31452492211838007, 0.3239424563728739, 0.35913349861520594, 0.32488393686165273, 0.23389261744966444, 0.23403361344537815, 0.038461538461538464, 0.0, 0.26666666666666666, 0.0, 0.5198198198198198, 0.6573295985060691, 0.19523809523809524, 0.5445553337768906, 0.4084507042253521, 0.4019927536231884, 0.3519230769230769, 0.0, 0.25925925925925924, 0.43851626016260165, 0.5551948051948052, 0.41931216931216925, 0.3562973484848485, 0.07692307692307693, 0.0, 0.45906432748538006, 0.14285714285714285, 0.2222222222222222, 0.25, 0.2, 0.0, 0.25, 0.0, 0.0, 0.0, 0.5818666666666666, 0.29411764705882354, 0.16666666666666666, 0.18181818181818182, 0.0, 0.0, 0.03508771929824561, 0.75, 0.25, 0.36046511627906974, 0.5052173913043478, 0.4826945412311266, 0.6438244047619047, 0.7407407407407407, 0.5, 0.7631578947368421, 0.0, 0.0, 0.07103825136612021, 0.0625]
    y_data_2 =  [0.5645713187235679, 0.44610591900311525, 0.4430212376534444, 0.4231943932591798, 0.3515718265021886, 0.4097762863534675, 0.3764705882352941, 0.20512820512820512, 0.3333333333333333, 0.3333333333333333, 0.0, 0.563963963963964, 0.633986928104575, 0.29047619047619044, 0.6006098913284541, 0.44366197183098594, 0.5016304347826087, 0.4647435897435897, 0.4375, 0.48148148148148145, 0.4176829268292683, 0.5797619047619047, 0.35582010582010576, 0.5411931818181818, 0.3076923076923077, 0.0, 0.5409356725146198, 0.42857142857142855, 0.4444444444444444, 0.5, 0.6, 0.0, 0.546875, 0.5833333333333334, 0.0, 0.14285714285714285, 0.6638666666666667, 0.5196078431372549, 0.08333333333333333, 0.4318181818181818, 0.0, 0.2, 0.32456140350877194, 0.8333333333333334, 0.4166666666666667, 0.19767441860465115, 0.7210144927536233, 0.4249709639953542, 0.5684523809523809, 0.7407407407407407, 0.75, 0.8157894736842105, 0.18181818181818182, 0.0, 0.21311475409836064, 0.21428571428571427]



    y_data_3 = [721, 544, 775, 1089, 198, 437,  58, 10, 2, 5, 0, 150, 38, 18, 400,  41, 158, 34, 8, 16,  91, 277,  58, 244, 1, 0,  53, 4,  4, 7, 8,  0,  15,  5,  0,  1,  91,  25, 2, 9, 0, 1,  23,  11, 7,  11, 115, 136, 173,  21, 3,  33, 3, 0,  42,  18]

    # y_data_4 = [654, 373, 546, 902, 180, 249, 34, 2, 0, 4, 0, 137, 44, 9, 352, 35, 126, 24, 0, 8, 86, 263, 63, 157, 1, 0, 43, 2, 2, 3, 3, 0, 8, 0, 0, 0, 76, 17, 2, 5, 0, 0, 2, 9, 4, 16, 82, 155, 197, 20, 2, 29, 0, 0, 13, 7]
    y_data_4 =[ 690, 532, 753, 1102, 185, 430, 55, 9, 1, 5, 0, 147, 41, 12, 391, 37, 157, 33, 7, 15, 84, 277, 54, 244, 4, 0, 50, 4, 4, 7, 9, 0, 19, 7, 0, 1, 88, 28, 1, 11, 0, 1, 19, 10, 5, 9, 115, 134, 169, 20, 3, 31, 3, 0, 40, 22]


    visual_data_by_line_bar(x_data, y_data_1, y_data_2, y_data_3, y_data_4)


