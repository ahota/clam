clam_colors = [
# carto prism
    '#5f4690', '#1d6996', '#38a6a5', '#0f8554',
    '#73af48', '#edad08', '#e17c05', '#cc503e',
    '#94346e', '#6f4070', '#994e95', '#666666'
# carto pastel
    '#66c5cc', '#f6cf71', '#f89c74', '#dcb0f2',
    '#87c55f', '#9eb9f3', '#fe88b1', '#c9db74',
    '#8be0a4', '#b497e7', '#d3b484', '#b3b3b3'
# carto bold
    '#7f3c8d', '#11a579', '#3969ac', '#f2b701',
    '#e73f74', '#80ba5a', '#e68310', '#008695',
    '#cf1c90', '#F97B72', '#4B4B8F', '#a5aa99'
# carto antique
    '#855c75', '#d9af6b', '#af6458', '#736f4c',
    '#526a83', '#625377', '#68855c', '#9c9c5e',
    '#a06177', '#8c785d', '#467378', '#7c7c7c'
# carto vivid
    '#e58606', '#5d69b1', '#52bca3', '#99c945',
    '#cc61b0', '#24796c', '#daa51b', '#2f8ac4',
    '#764e9f', '#ed645a', '#cc3a8e', '#a5aa99'
# mpl tab20 b/c interleaved
    '#393b79', '#637939', '#8c6d31', '#843c39',
    '#7b4173', '#3182bd', '#e6550d', '#31a354',
    '#756bb1', '#636363', '#5254a3', '#8ca252',
    '#bd9e39', '#ad494a', '#a55194', '#6baed6',
    '#fd8d3c', '#74c476', '#9e9ac8', '#969696',
    '#6b6ecf', '#b5cf6b', '#e7ba52', '#d6616b',
    '#ce6dbd', '#9ecae1', '#fdae6b', '#a1d99b',
    '#bcbddc', '#bdbdbd', '#9c9ede', '#cedb9c',
    '#e7cb94', '#e7969c', '#de9ed6', '#c6dbef',
    '#fdd0a2', '#c7e9c0', '#dadaeb', '#d9d9d9'
]


def build_colors(n):
    if n <= len(clam_colors):
        return clam_colors[:n]
    else:
        repeat = n // len(clam_colors)
        remain = len(clam_colors) % n
        return clam_colors*repeat + clam_colors[:remain]
