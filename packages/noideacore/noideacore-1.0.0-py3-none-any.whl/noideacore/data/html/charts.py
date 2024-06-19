
colors = [
    "#FF6384",  # Rotes Rosa
    "#36A2EB",  # Blaues Türkis
    "#FFCE56",  # Gelb
    "#4BC0C0",  # Türkis
    "#9966FF",  # Lila
    "#FF8A80",  # Hellrot
    "#1E88E5",  # Dunkles Blau
    "#FFD54F",  # Orange
    "#4DB6AC",  # Grünblau
    "#7CB342",  # Grün
    "#F06292",  # Rosa
    "#9575CD",  # Hellviolett
    "#64B5F6",  # Himmelblau
    "#FFB74D",  # Orange
    "#81C784",  # Hellgrün
    "#7986CB",  # Blauviolett
    "#A1887F",  # Braungrau
    "#90A4AE",  # Blaugrau
]

def full_build(labels:list, data:dict, name:str = 'myChart', width_height = (100, 100), title ='Chart.js Line Chart', type ='line'):
    return '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', f'<canvas id="{name}" width="{width_height[0]}" height="{width_height[1]}"></canvas>',f'''<script>const xValues = {labels}; const data = {build_data(data)}; const config = {build_config(title, type)}; {name} = new Chart("{name}", config); </script>'''

def make_colors(data:dict):
    color_num = 0
    for x in data.keys():
        if color_num == len(colors):
            color_num = 0
        data[x].append(colors[color_num])
        color_num += 1

def build_data(data:dict):
    make_colors(data)
    datas = list()
    for x in data.keys():
        js_data = f'''{{label: '{x}', data: {data[x][0:-1]}, borderColor: "{data[x][-1]}", fill: false}}'''
        datas.append(js_data)
    datas = ', '.join(datas)
    full_data = f'''{{labels: xValues, datasets: [{datas}]}}'''
    return full_data

def build_config(title = 'Chart.js Line Chart', type = 'line'):
    config_data = f'''{{type: '{type}', data: data, options: {{ responsive: true, plugins: {{ legend: {{ position: 'top', }}, title: {{ display: true, text: '{title}' }} }} }}, }};'''
    return config_data
