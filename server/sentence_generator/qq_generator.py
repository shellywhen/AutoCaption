def generate_toy_qq_sentence(focal_array, data):

    num = len(focal_array[1]['focus_id'])
    prep = 'is'
    outlier = 'outlier'
    if num > 1:
        prep = 'are'
        outlier = 'outliers'
    explicit = ''
    for i, id  in enumerate(focal_array[1]['focus_id']):
        if(i>0):
            explicit+=', '
        explicit+=getPoint(data['data_array'][id]['q0'], data['data_array'][id]['q1'])
    sentences = [{
    'type': 'cluster',
    'sentence': 'There is a cluster in the chart.',
    'compare_id': focal_array[0]['compare_id'],
    'focus_id': focal_array[0]['focus_id'],
    'strength': focal_array[0]['strength']
    }, {
    'type': 'outlier',
    'sentence': f'There {prep} {num} {outlier} in total, which {prep} {explicit}.',
    'compare_id': focal_array[1]['compare_id'],
    'focus_id': focal_array[1]['focus_id'],
    'strength': focal_array[1]['strength']
    }]
    print('mysentences', sentences)
    return sentences

def getPoint(x, y):
    line = '(' + str(round(x, 2)) + ',' + str(round(y,2)) + ')'
    return line
