import random


def generate_data(num):
    income_list = []
    key = 'income-list'
    for i in range(0, num):
        net_code = random.choice(['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                                  '144', '147', '149', '150', '151', '152', '153', '155', '156', '157', '158', '159',
                                  '166', '170', '171', '172', '173', '174', '175', '176', '177', '178', '180', '181',
                                  '182', '183', '184', '185', '186', '187', '188', '189', '190', '191', '193', '195', '196', '199'])
        suffix = ''.join(random.sample('0123456789', 6))
        income = str(int(random.uniform(1, 10) * 1000000) / 1000000)
        income_list.append({'user': 'XY' + suffix, 'income': income})
    return {'results': income_list}
