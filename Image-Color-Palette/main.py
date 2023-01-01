from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import extcolors
from colormap import rgb2hex
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "Jahnavi12345"


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        image = request.form['choosen-image']

        for root, dirs, files in os.walk('C:/'):
            for name in files:
                if image in name:
                    image_selected = os.path.abspath(os.path.join(root, name))
                    print(image_selected)
                    print(image)
                    tolerance_selected = int(request.form['tolerance'])
                    colors = int(request.form['colors'])

                    def color_to_df(input):
                        colors_pre_list = str(input).replace('([(', '').split(', (')[0:-1]
                        print(colors_pre_list)
                        df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
                        print(df_rgb)
                        df_percent = [i.split('), ')[1].replace(')', '') for i in colors_pre_list]
                        print(df_percent)
                        # convert RGB to HEX code
                        df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                                               int(i.split(", ")[1]),
                                               int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]
                        print(df_color_up)
                        df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurence'])
                        return df

                    img_url = image_selected

                    colors_x = extcolors.extract_from_path(img_url, tolerance=tolerance_selected, limit=colors+1)
                    print(colors_x)

                    df_color = color_to_df(colors_x[0: 20])
                    print(df_color)

                    list_color = list(df_color['c_code'])
                    print(list_color[0], type(list_color[0]))
                    list_percent = [int(i) for i in list(df_color['occurence'])]
                    text_c = [c + ' ' + str(round(p * 100 / sum(list_percent), 1)) + '%' for c, p in zip(list_color, list_percent)]

                    fig, ax = plt.subplots(figsize=(300, 108), dpi=10)
                    print(fig, ax)
                    fig.set_facecolor('white')
                    plt.savefig('static/bg.png')
                    plt.close(fig)
                    img = mpimg.imread(image_selected)
                    bg = plt.imread('static/bg.png')

                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(550, 200), dpi=10)

                    # donut plot
                    wedges, text = ax1.pie(list_percent,
                                          labels=text_c,
                                          labeldistance=1.05,
                                          colors=list_color,
                                          textprops={'fontsize': 250, 'color':'black'})
                    plt.setp(wedges, width=0.3)

                    # add image in the center of donut plot
                    imagebox = OffsetImage(img, zoom=6.2)
                    ab = AnnotationBbox(imagebox, (0, 0))
                    ax1.add_artist(ab)

                    x_posi, y_posi, y_posi2, y_pos3, y_pos4 = 300, 25, 25, 25, 25
                    for c, p in zip(list_color, list_percent):
                        if list_color.index(c) < 5:
                            y_posi += 125
                            rect = patches.Rectangle((x_posi, y_posi), 180, 80, facecolor=c)
                            ax2.add_patch(rect)
                            ax2.text(x=x_posi + 210, y=y_posi + 50, s=c + " " + str(round(p*100/sum(list_percent), 1)) + "%", fontdict={'fontsize': 300})
                        elif list_color.index(c) < 10 and list_color.index(c) >= 5:
                            y_posi2 += 125
                            rect = patches.Rectangle((x_posi + 580, y_posi2), 180, 80, facecolor=c)
                            ax2.add_artist(rect)
                            ax2.text(x=x_posi + 770, y=y_posi2 + 50, s=c + " " + str(round(p*100/sum(list_percent), 1)) + "%", fontdict={'fontsize': 300})
                        elif list_color.index(c) < 15 and list_color.index(c) >= 10:
                            y_pos3 += 125
                            rect = patches.Rectangle((x_posi + 1150, y_pos3), 180, 80, facecolor=c)
                            ax2.add_artist(rect)
                            ax2.text(x=x_posi + 1340, y=y_pos3 + 50, s=c + " " + str(round(p*100/sum(list_percent), 1)) + "%", fontdict={'fontsize': 300})
                        else:
                            y_pos4 += 125
                            rect = patches.Rectangle((x_posi + 1720, y_pos4), 180, 80, facecolor=c)
                            ax2.add_artist(rect)
                            ax2.text(x=x_posi + 1910, y=y_pos4 + 50, s=c + " " + str(round(p*100/sum(list_percent), 1)) + "%", fontdict={'fontsize': 350})


                    ax2.axis('off')
                    fig.set_facecolor('white')
                    plt.imshow(bg)
                    plt.tight_layout()
                    plt.savefig("static/palette.png")
                    return redirect(url_for('home'))
    else:
        return render_template("index.html")


if __name__ == "__main__":
   app.run(debug=True)