import io
import matplotlib.pyplot as plt

def construir_grafico(entrada):
    #print("Inicia proceso ")
    #entrada = request.get_json()
    #print(str(entrada))
    x = entrada['x']
    series = entrada['series']

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if 'title' in entrada.keys():
        ax.set_title( entrada['title'] )

    if 'xlabel' in entrada.keys():
        ax.set_xlabel( entrada['xlabel'] )

    if 'ylabel' in entrada.keys():
        ax.set_ylabel( entrada['ylabel'] )

    if 'grid' in entrada.keys():
        ax.grid(entrada['grid'])
    #print("pro procesar series")
    for serie in series:
        tipo = serie['tipo']
        y = serie['y']

        color = 'black'
        if 'color' in serie.keys():
            color = serie['color']

        label = 'Sin Label'
        if 'label' in serie.keys():
            label = serie['label']

        marker = 'None'
        if 'marker' in serie.keys():
            marker = serie['marker']

        if tipo == 'scatter':
            z = serie['z']
            ax.scatter(x,y,c = z, label = label)
        elif tipo == 'plot':
            ax.plot(x,y, color= color, marker= marker, label = label)
        elif tipo == 'pie':
            labels = serie['labels']
            startangle = 0
            if 'startangle' in serie.keys():
                startangle = serie['startangle']
            autopct = '%1.1f%%'
            if 'autopct' in serie.keys():
                autopct = serie['autopct']
            ax.pie(y,labels = labels, startangle = startangle, autopct=autopct)
        elif tipo == 'hist':
            bins = 5
            if 'bins' in serie.keys():
                bins = serie['bins']
            normed = False
            if 'normed' in serie.keys():
                normed = serie['normed']
            ax.hist(y, color = color, bins = bins , normed = normed)
        elif tipo == 'boxplot':
            labels = serie['labels']
            notch = False
            if 'notch' in serie.keys():
                notch = serie['notch']
            bootstrap = 1
            if 'bootstrap' in serie.keys():
                bootstrap = serie['bootstrap']
            vert = True
            if 'vert' in serie.keys():
                vert = serie['vert']
            ax.boxplot(y, labels = labels, notch = notch, bootstrap = bootstrap, vert = vert)

    if 'legend' in entrada.keys() and entrada['legend'] == True :
        ax.legend()

    salida = io.BytesIO()
    plt.savefig(salida, format='png')
    return salida
